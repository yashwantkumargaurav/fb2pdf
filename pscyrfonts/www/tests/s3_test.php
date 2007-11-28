<?php
require_once 'awscfg.php';
require_once 's3.php';

global $awsApiKey, $awsApiSecretKey;

$op = $_GET['op'];
if (!$op)
    die("use s3_test?op={write|delete}");

$bucket = "fb2pdf_debug";
$filename = "test2.fb2";

$filepath = "http://" . $_SERVER["HTTP_HOST"]. rtrim(dirname($_SERVER["PHP_SELF"]), "/\\") . "/$filename";

$s3 = new S3($awsApiKey, $awsApiSecretKey);

$op = $_GET['op'];
if ($op == 'delete')
{
    $s3->deleteObject($bucket, $filename);
    
    //header("content-type: text/xml");
    print ("Response code = $s3->responseCode");
    print ("<br>Response Header:<br>");
    print_r ($s3->responseHeader);
    print ("<br>Response Body:<br>");
    print ($s3->responseBody);
}
else if ($op == 'write')
{
    $httpHeaders = array("Content-Disposition"=>"attachement; filename=\"$filename\"");
    $s3->writeFile($bucket, $filename, $filepath, "text/xml", "public-read", "", $httpHeaders);

    //header("content-type: text/xml");
    print ($s3->responseCode);
    //print ($s3->responseBody);
}
?>