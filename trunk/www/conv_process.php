<?php
require_once 'utils.php';

if (!isset ($_GET["url"]))
{
    httpResponseCode("400 Bad Request", "Missing paremeter \"url\"");
    die;
}

//TODO. donwload and process book
$url = $_GET["url"];
$md5 = md5($url);
$title = "some title";
$author = "some author";

// generate response xml
header('HTTP/1.0 200 OK');
header('Content-type: text/xml');    

echo '<?xml version="1.0" encoding="UTF-8"?>';
echo '<fb2pdfconv version="1.0">';
echo "<key>$md5</key>";
echo "<author>$author</author>";
echo "<title>$title</title>";
echo '</fb2pdfconv>';

?>