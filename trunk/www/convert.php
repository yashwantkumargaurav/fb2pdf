<?php

if (!isset ($_GET["url"]))
{
    header("HTTP/1.0 400 Bad Request");
    header('Content-type: text/html');    
    echo "<html><body>Missing \"url\" parameter</body></html>";
}
else
{
    // redirect to the index page
    $url = $_GET["url"];
    if (isset ($_GET["auto"]))
    {
        header("HTTP/1.0 302 Found");
        header("Location: uploader.php?url=$url");
    }
    else
    {
        header("HTTP/1.0 302 Found");
        header("Location: index.php?url=$url");
    }
}
?>