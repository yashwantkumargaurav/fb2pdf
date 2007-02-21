<?php
require_once 'awscfg.php';
require_once 's3.php';

// Put file to amazon s3
function store_file($filePath)
{
    global $awsApiKey, $awsApiSecretKey, $awsS3Bucket;

    // S3
    $s3 = new S3($awsApiKey, $awsApiSecretKey);

    // create an object
    $metadata = array("status"=>"", "result"=>"");
    if (!$s3->createObject($awsS3Bucket, "test", "blah-blah", "text/html", "public-read", $metadata))
        die ("Error creating object");
        
    $meta = $s3->getObjectMetadata($awsS3Bucket, "test");
    print("Got methadata:<br>");
    print_r($meta);
    
    
    return TRUE;
}
  
?>