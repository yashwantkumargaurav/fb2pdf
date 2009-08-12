<?php
require_once 'utils.php';
require_once 'process.php';

header("Cache-Control: must-revalidate, post-check=0, pre-check=0");

if (isset ($_GET["key"]) and isset ($_GET["format"]))
{
    $key = $_GET["key"];
    $format = $_GET["format"];
    
    $conv = new ConvertBook();
    try
    {
        $conv->convertFromS3($key, $format);
        httpRedirect("status.php?key=$key&format=$format");
    }
    catch(Exception $e)
    {
        error_log("FB2PDF ERROR. Convert: " . $e->getMessage());
        httpResponseCode("400 Bad Request", "Ошибка конвертации. Пожалуйста, попробуйте ешё раз.");
    }
}
else if (isset ($_GET["url"]))
{
    // redirect to the index page
    $url = $_GET["url"];
    if (isset ($_GET["auto"]))
        httpRedirect("uploader.php?url=$url");
    else
        httpRedirect("index.php?url=$url");
}
else
{
    httpResponseCode("400 Bad Request", "Missing parameter \"url\"");
}
?>