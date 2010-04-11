<?php
require_once 'process.php';
require_once 'utils.php';

if (!isset ($_GET["key"]))
{
    httpResponseCode("400 Bad Request", "Missing parameter \"key\"");
    die;
}

$key = $_GET["key"];
$format = $_GET["format"];
$bs = new BookStatus();
try
{
    $bs->checkOriginal($key);
    $status = $bs->checkConverted($key, $format);
    
    // generate response json
    header('Content-type: application/json');    

    $response = 
    "{
        'status'    : '$status',
        'source'    : '$bs->fbFile',
        'converted' : '$bs->pdfFile',
        'log'       : '$bs->logFile'
    }";
    echo $response;
}
catch(Exception $e)
{
    error_log("FB2PDF ERROR. Status: " . $e->getMessage()); 
    httpResponseCode("400 Bad Request", $e->getMessage());
}

?>