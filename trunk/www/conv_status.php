<?php
require_once 'utils.php';

if (!isset ($_GET["key"]))
{
    httpResponseCode("400 Bad Request", "Missing paremeter \"key\"");
    die;
}

$key = $_GET["key"];

//TODO. check book status
$rand = rand(0,2);
if ($rand == 0)
    $status = 'p';
else if ($rand == 1)
    $status = 'r';
else
    $status = 'e';

$source    = "$key.fb2";
$converted = "$key.pdf";
$log       = "$key.txt";
    
// generate response xml
header('Content-type: application/json');    

$response = 
"{
    'status'    : '$status',
    'source'    : '$source',
    'converted' : '$converted',
    'log'       : '$log'
}";
echo $response;
?>