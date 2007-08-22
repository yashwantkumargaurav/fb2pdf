<?php
require_once 'fbparser.php';
require_once 'zipparser.php';
require_once 'awscfg.php';
require_once 's3.php';
require_once 'sqshelper.php';
require_once 'db.php';
require_once 'utils.php';

$testMode = false; // set to false for production

$filePath = NULL;
$fileName = NULL;
$tempFile = tempnam(md5(uniqid(rand(), TRUE)), '');

$url = (isset($_GET["url"])) ? $_GET["url"] : NULL;

if ($url || $_POST['uploadtype'] == 'url')
{
    $filePath = ($url) ? $url : $_POST['url'];
    $fileName = $filePath;
    
    if (!copy($filePath, $tempFile))
        die("Внутренняя ошибка системы. Невозможно загрузить файл. Пожалуйста, попробуйте ешё раз.");
        
    $filePath = $tempFile;
}
else if ($_POST['uploadtype'] == 'file')
{
    // check uploaded file
    $filePath = $_FILES['fileupload']['tmp_name'];
    $fileName = $_FILES['fileupload']['name'];
    
    if (trim($fileName) == "")
        die("Пожалуйста, укажите FB2 файл, который Вы бы хотели сконвертировать.");
        
    if (!move_uploaded_file($filePath, $tempFile)) 
        die("Внутренняя ошибка системы. Невозможно загрузить файл. Пожалуйста, попробуйте ешё раз.");
        
    $filePath = $tempFile;
}
$email = $_POST['email'];

// Check zip format
$zipArr = check_zip_format($filePath);
if ($zipArr === false) //  not a zip file
{
    $zipFile = NULL;
    $fbFile  = $filePath;
    
    $parser = new FBParser();
    if (!$parser->parse($fbFile))
        die("$fileName не существует или не является файлом в формате ZIP или FB2. Пожалуйста, выберите ZIP или FB2 файл и попробуйте ещё раз.");
    $bookTitle  = $parser->getTitle();
    $bookAuthor = $parser->getAuthor();
    $isbn       = $parser->getIsbn();
}
else // zip file
{
    $zipFile    = $filePath;
    $fbFile     = $zipArr["filePath"];
    $fileName   = $zipArr["fileName"];
    $bookTitle  = $zipArr["bookTitle"];
    $bookAuthor = $zipArr["bookAuthor"];
    $isbn       = $zipArr["isbn"];
}

// Process file
$key = process_file($fbFile, $fileName, $email, $bookTitle, $bookAuthor, $isbn);

// remove temporary files
if ($zipFile and !unlink($zipFile))
    error_log("FB2PDF WARN. Unable to remove temporary file <$zipFile>"); 
if ($fbFile and !unlink($fbFile))
    error_log("FB2PDF WARN. Unable to remove temporary file <$fbFile>"); 
    
if ($key === false)
    die("Невозможно сохранить файл $fileName для дальнейшей конвертации. Пожалуйста, попробуйте ешё раз.");

// redirect to the status page
header("HTTP/1.0 302 Found");
header("Location: status.php?id=$key");

// Process file.
// Returns key or false
function process_file($filePath, $fileName, $email, $bookTitle, $bookAuthor, $isbn)
{
    global $awsApiKey, $awsApiSecretKey, $awsS3Bucket, $testMode, $secret;
    global $dbServer, $dbName, $dbUser, $dbPassword;
    global $convVersion;

    // genarate key
    $key = md5(uniqid(""));
    
    // get md5 of the file content
    $md5 = md5($fileName);
    
    // get the filename without extension
    $pathParts = pathinfo($fileName);
    $name = $pathParts["basename"];
    $pos = strrpos($name, ".");
    if ($pos !== false) 
        $name = substr($name, 0, $pos);

    if (!$name) // if name is empty
        $name = $key;
    
    if (!$testMode)
    {
        $db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
        
        // check if this book already exists
        $isNewBook = true;
        $bookInfo = $db->getBook($md5);
        if ($bookInfo)
        {
            $key = $bookInfo["storage_key"];
            // check error status and converter version
            $bookStatus = $bookInfo["status"];
            $bookVer    = $bookInfo["conv_ver"];
            if (($bookStatus == 'r' and $bookVer >= $convVersion) or $bookStatus == 'p') 
            {
                // send email to user
                if ($email)
                    notifyUserByEmail($email, $key);
                
                return $key;
            }
            else 
            {
                error_log("FB2PDF INFO. Books $key needs to be converted again. Status=$bookStatus, Version=$bookVer"); 
                $isNewBook = false;
            }
        }
        
        // create an object to store source file
        $s3 = new S3($awsApiKey, $awsApiSecretKey);

        if ($isNewBook)
        {
            $httpHeaders = array("Content-Disposition"=>"attachement; filename=\"$name.fb2\"");
            if (!$s3->writeFile($awsS3Bucket, $key . ".fb2", $filePath, "application/fb2+xml", "public-read", "", $httpHeaders))
            {
                error_log("FB2PDF ERROR. Unable to store file with key <$key> in the Amazon S3 storage."); 
                return false;
            }
            
            // save to DB
            if (!$db->insertBook($key . ".zip", $bookAuthor, $bookTitle, $isbn, $md5, "p"))
            {
                error_log("FB2PDF ERROR. Unable to insert book with key <$key> into DB."); 
                // do not stop if DB is failed!
            }
        }
        else
        {
            // update book status in the DB
            if (!$db->updateBookStatus($key, "p", 0))
            {
                error_log("FB2PDF ERROR. Callback: Unable to update book status. Key=$key"); 
                // do not stop if DB is failed!
            }
            
            // remove result/log file
            $pos = strrpos($key, ".");
            if ($pos !== false) 
                $key = substr($key, 0, $pos);
                
            if (!$s3->deleteObject($awsS3Bucket, $key . ".zip"))
            {
                error_log("FB2PDF ERROR. Unable to delete converted file <$key.zip> from the Amazon S3 storage."); 
                // do not stop if failed!
            }
            
            if (!$s3->deleteObject($awsS3Bucket, $key . ".txt"))
            {
                error_log("FB2PDF ERROR. Unable to delete log file <$key.txt> from the Amazon S3 storage."); 
                // do not stop if failed!
            }
        }
        
        // send SQS message
        $callbackUrl = getFullUrl("conv_callback.php");
        if(!sqsPutMessage($key, "http://s3.amazonaws.com/$awsS3Bucket/$key.fb2", $name, $callbackUrl, md5($secret . $key . ".zip"), $email))
        {
            error_log("FB2PDF ERROR. Unable to send Amazon  SQS message for key <$key>."); 
            return false;
        }
    }    
    return $key;
}

?>
