<?php
require_once 'fbparser.php';
require_once 'zipparser.php';
require_once 'awscfg.php';
require_once 's3.php';
require_once 'sqshelper.php';

$testMode = false; // set to false for production

$filePath = NULL;
$fileName = NULL;
$tempFile = tempnam(md5(uniqid(rand(), TRUE)), '');

if ($_POST['uploadtype'] == 'file')
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
else if ($_POST['uploadtype'] == 'url')
{
    $filePath = $_POST['url'];
    $fileName = $filePath;
    
    if (!copy($filePath, $tempFile))
        die("Внутренняя ошибка системы. Невозможно загрузить файл. Пожалуйста, попробуйте ешё раз.");
        
    $filePath = $tempFile;
}

// Check zip format
$zipFile = $filePath;
$fbFile = check_zip_format($zipFile);
if ($fbFile === false) // this is not a zip
{
    $fbFile = $zipFile;
    $zipFile = NULL;
    if (!check_fb_format($fbFile))
        die("$fileName не существует или не является файлом в формате ZIP или FB2. Пожалуйста, выберите ZIP или FB2 файл и попробуйте ещё раз.");
}

// Process file
$key = process_file($fbFile, $fileName);

// remove temporary files
if ($zipFile and !unlink($zipFile))
    error_log("FB2PDF WARN. Unable to remove temporary file <$zipFile>"); 
if ($fbFile and !unlink($fbFile))
    error_log("FB2PDF WARN. Unable to remove temporary file <$fbFile>"); 
    
if ($key === false)
    die("Невозможно сохранить файл $fileName для дальнейшей конвертации. Пожалуйста, попробуйте ешё раз.");

// redirect to the status page
$host = $_SERVER["HTTP_HOST"];
$uri  = rtrim(dirname($_SERVER["PHP_SELF"]), "/\\");
$page = "status.php?id=$key";

$url = "http://$host$uri/$page";
header("Location: $url");

// Process file.
// Returns key or false
function process_file($filePath, $fileName)
{
    global $awsApiKey, $awsApiSecretKey, $awsS3Bucket, $testMode;

    // genarate key
    $md5 = md5(uniqid(""));
    
    // get the filename without extension
    $pathParts = pathinfo($fileName);
    $name = $pathParts["basename"];
    $pos = strrpos($name, ".");
    if ($pos !== false) 
        $name = substr($name, 0, $pos);

    if (!$testMode)
    {
        // content-disposition
        $httpHeaders = array("Content-Disposition"=>"attachement; filename=\"$name.fb2\"");
        
        // create an object to store source file
        $s3 = new S3($awsApiKey, $awsApiSecretKey);

        if (!$s3->writeObject($awsS3Bucket, $md5 . ".fb2", $filePath, "application/fb2+xml", "public-read", "", $httpHeaders))
        {
            error_log("FB2PDF ERROR. Unable to store file with key <$md5> in the Amazon S3 storage."); 
            return false;
        }
        
        // send SQS message
        if(!sqsPutMessage($md5, "http://s3.amazonaws.com/$awsS3Bucket/$md5.fb2", $name))
        {
            error_log("FB2PDF ERROR. Unable to send Amazon  SQS message for key <$md5>."); 
            return false;
        }
    }    
    return $md5;
}
?>
