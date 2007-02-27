<?php
require_once 'fbparser.php';
require_once 'awscfg.php';
require_once 's3.php';
require_once 'sqshelper.php';

$filePath = NULL;
$fileName = NULL;

if ($_POST['uploadtype'] == 'file')
{
    // check uploaded file
    $filePath = $_FILES['fileupload']['tmp_name'];
    $fileName = $_FILES['fileupload']['name'];
    
    if (trim($fileName) == "")
        die("Пожалуйста, укажите FB2 файл, который Вы бы хотели сконвертировать.");
        
    if (!is_uploaded_file($filePath)) 
        die("Внутренняя ошибка системы. Невозможно загрузить файл. Пожалуйста, попробуйте ешё раз.");
}
else if ($_POST['uploadtype'] == 'url')
{
    $filePath = $_POST['url'];
    $fileName = $filePath;
}

// Check format
if (!check_fb_format($filePath))
    die($fileName . " не существует или не является файлом в формате FB2. Пожалуйста, выберите FB2 файл и попробуйте ещё раз.");

// Process file
$key = process_file($filePath, $fileName);
if ($key === false)
    die("Невозможно сохранить файл " . $fileName . " для дальнейшей конвертации. Пожалуйста, попробуйте ешё раз.");

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
    global $awsApiKey, $awsApiSecretKey, $awsS3Bucket;

    // get file content
    $data = file_get_contents($filePath);
    //$md5 = md5(data);
    $md5 = md5(uniqid(""));
    
    // get the filename without extension
    $pathParts = pathinfo($fileName);
    $name = $pathParts["basename"];
    $pos = strrpos($name, ".");
    if ($pos !== false) 
        $name = substr($name, 0, $pos);

    // content-disposition
    $httpHeaders = array("Content-Disposition"=>"attachement; filename=\"$name.fb2\"");
    
    // create an object to store source file
    $s3 = new S3($awsApiKey, $awsApiSecretKey);

    if (!$s3->writeObject($awsS3Bucket, $md5 . ".fb2", $data, "application/fb2+xml", "public-read", "", $httpHeaders))
        return false;
    
    // send SQS message
    if(!sqsPutMessage($md5, "http://s3.amazonaws.com/$awsS3Bucket/$md5.fb2", $name))
        return false;
    
    return $md5;
}
?>
