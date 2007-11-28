<?php
require_once 'awscfg.php';
require_once 'HTTP/Request.php';

global $secret;

$key = "25d34598d6c62c9bcdc8e67daf792fb9.pdf";
$email = "123@test.com";
$status = "r";
$password = md5($secret . $key);
error_log("TEST password=$password");


$httpDate = gmdate('D, d M Y H:i:s T');
$request =& new HTTP_Request("conv_callback.php");
$request->setMethod("POST");
$request->addHeader("Date", $httpDate);
$request->addHeader("content-type", "multipart/form-data");

$request->addPostData("pass",   $password);
$request->addPostData("email",  $email);
$request->addPostData("key",    $key);
$request->addPostData("status", $status);

$request->sendRequest();

header("content-type: text/html");
print ($request->getResponseCode()."<br>".$request->getResponseBody());
?>
