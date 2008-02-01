<?php
require_once '../awscfg.php';
require_once '../db.php';
require_once '../s3.php';
require_once '../utils.php';

if (!isset ($_GET['key']))
{
    httpResponseCode("400 Bad Request", "Missing parameter \"key\"");
    die;
}
$key = $_GET['key'];

$pos = strrpos($key, ".");
if ($pos !== false) 
    $key = substr($key, 0, $pos);

$msg = "";

$db = getDBObject();
if (!$db->deleteBook($key . ".zip"))
    $msg .= "<br>Unable to delete $key.zip from DB";
    

global $awsS3Bucket;

$s3 = getS3Object();

if (!$s3->deleteObject($awsS3Bucket, $key . ".fb2"))
    $msg .= "<br>Unable to delete file $key.fb2 from Amazon S3";

if (!$s3->deleteObject($awsS3Bucket, $key . ".zip"))
    $msg .= "<br>Unable to delete file $key.zip from Amazon S3";

if (!$s3->deleteObject($awsS3Bucket, $key . ".log"))
    $msg .= "<br>Unable to delete file $key.log from Amazon S3";

if ($msg)
    echo $msg;
else    
    echo "Delete book $key - done."
?>