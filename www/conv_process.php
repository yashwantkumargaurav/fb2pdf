<?php
require_once 'process.php';
require_once 'utils.php';

if (!isset ($_GET["url"]))
{
    httpResponseCode("400 Bad Request", "Missing paremeter \"url\"");
    die;
}

try
{
    $conv = new ConvertBook();
    $conv->convertFromUrl($_GET["url"]);
    
    $key    = $conv->bookKey;
    $author = $conv->book->author;
    $title  = $conv->book->title;

    // generate response
    header('HTTP/1.0 200 OK');
    header('Content-type: application/json');    

    $response = 
    "{
        'key'   : '$key',
        'author': '$author',
        'title' : '$title'
    }";
    echo $response;
}
catch(Exception $e)
{
    $errCode = null;
    
    if ($e->getCode() == ConvertBook::ERR_ILLEGAL_ARG)
        $errCode = "400 Bad Request";
    else if ($e->getCode() == ConvertBook::ERR_LOAD)
        $errCode = "400 Bad Request";
    else if ($e->getCode() == ConvertBook::ERR_FORMAT)
        $errCode = "404 Not Found";
    else if ($e->getCode() == ConvertBook::ERR_CONVERT)
        $errCode = "500 Internal Server Error";
    
    error_log("FB2PDF ERROR. Status: " . $e->getMessage()); 
    httpResponseCode($errCode, $e->getMessage());
}
?>