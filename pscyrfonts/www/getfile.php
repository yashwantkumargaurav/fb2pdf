<?php
require_once 'awscfg.php';
require_once 'db.php';

global $awsS3Bucket;
global $dbServer, $dbName, $dbUser, $dbPassword;

if (!isset ($_GET["key"]))
{
    header("HTTP/1.0 400 Bad Request");
    header('Content-type: text/html');    
    echo "<html><body>Missing \"key\" paremeter</body></html>";
}
else
{
    $key = $_GET["key"];
    $url = "http://s3.amazonaws.com/$awsS3Bucket/$key";

    // update counter in the DB
    if (strstr($key, ".zip") or strstr($key, ".pdf"))
    {
        $db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
        if (!$db->updateBookCounter($key))
            error_log("FB2PDF ERROR. Unable to update book's counter. Key=$key"); 
    }
    
    header("HTTP/1.0 302 Found");
    header("Location: $url");
    
}

?>