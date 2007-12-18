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
header('HTTP/1.0 200 OK');
header('Content-type: text/xml');    

echo '<?xml version="1.0" encoding="UTF-8"?>';
echo '<fb2pdfstatus version="1.0">';
echo "<status>$status</status>";
echo "<source>$source</source>";
echo "<converted>$converted</converted>";
echo "<log>$log</log>";
echo '</fb2pdfstatus>';

?>