<?php
require_once 'process.php';
require_once 'utils.php';

if (!isset ($_GET["key"]))
{
    httpResponseCode("400 Bad Request", "Missing parameter \"key\"");
    die;
}

$bs = new BookStatus();
try
{
    $status = $bs->checkStatus($_GET["key"]);
    
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