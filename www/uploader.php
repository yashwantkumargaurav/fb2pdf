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
        die("Please, specify a file you would like to convert.");
        
    if (!is_uploaded_file($filePath)) 
        die("Internal error. Unable to upload the file. Please, try again.");
}
else if ($_POST['uploadtype'] == 'url')
{
    $filePath = $_POST['url'];
    $fileName = $filePath;
}

// Check format
if (!check_fb_format($filePath))
    die($fileName . " does not exists or it is not a fb2 file. Please select a fb2 file and try again.");

// Process file
$key = process_file($filePath, $fileName);
if ($key === false)
    die("Unable to store file " . $fileName . " for further processing. Please try again.");

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
    $md5 = md5(data);
    
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
