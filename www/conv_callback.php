<?php
require_once 'process.php';
require_once 'utils.php';

$password = trim($_POST['pass']);
$email    = trim($_POST['email']);
$key      = trim($_POST['key']);
$status   = trim($_POST['status']);

if (isset ($_POST['ver']))
    $ver = trim($_POST['ver']);
else
    $ver = 0;

if (isset ($_POST['format']))
    $format = trim($_POST['format']);

if (!$format || $format == '') 
        $format = 1;
try
{
    $conv = new ConvertBook();
    $conv->converted($email, $password, $key, $status, $ver, $format);
    
    httpResponseCode("200 OK");
}
catch(Exception $e)
{
    error_log("FB2PDF ERROR. Callback: " . $e->getMessage()); 
    httpResponseCode("400 Bad Request", $e->getMessage());
}
?>
