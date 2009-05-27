<?php
require_once 'awscfg.php';
require_once 'db.php';
require_once 'utils.php';

global $awsS3Bucket;

if (!isset ($_GET["key"]))
{
    httpResponseCode("400 Bad Request", "Missing parameter \"key\"");
}
else
{
    $key = $_GET["key"];
    $format = $_GET["format"];
    $url = "http://s3.amazonaws.com/$awsS3Bucket/$key";

    // update counter in the DB
    if (strstr($key, ".zip") or strstr($key, ".pdf"))
    {
        $db = getDBObject();
        if (!$db->updateBookCounter($key, $format))
            error_log("FB2PDF ERROR. Unable to update book's counter. Key=$key"); 
    }
    
    httpRedirect($url);
}

?>