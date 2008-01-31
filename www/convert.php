<?php
require_once 'utils.php';

if (!isset ($_GET["url"]))
{
    httpResponseCode("400 Bad Request", "Missing parameter \"url\"");
}
else
{
    // redirect to the index page
    $url = $_GET["url"];
    if (isset ($_GET["auto"]))
        httpRedirect("uploader.php?url=$url");
    else
        httpRedirect("index.php?url=$url");
}
?>