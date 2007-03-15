<?php
require_once 'awscfg.php';

global $awsS3Bucket;

if (!isset ($_GET["key"]))
{
    header("HTTP/1.0 400 Bad Request");
    header('Content-type: text/html');    
    echo "<html><body>Missing \"key\" paremeter</body></html>";
}
else
{
    $url    = "http://s3.amazonaws.com/$awsS3Bucket/" . $_GET["key"];
    header("HTTP/1.0 302 Found");
    header("Location: $url");
    
}

?>