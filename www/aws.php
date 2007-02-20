<?php
require_once 'awscfg.php';
require_once 's3.class.php';

// Put file to amazon s3
function store_file($filePath)
{
    global $awsApiKey, $awsApiSecretKey, $awsS3Bucket;

    // S3
    $s3 = new S3();
    $s3->keyId = $awsApiKey;
    $s3->secretKey = $awsApiSecretKey;

    // create a bucket
    $s3->putBucket($awsS3Bucket);
    
    // create a file with metadata
    
    return TRUE;
}
    

?>