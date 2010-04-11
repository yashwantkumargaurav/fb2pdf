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
            
    $url = "http://s3.amazonaws.com/$awsS3Bucket/$key";

    // update counter in the DB
    if (strstr($key, ".zip") or strstr($key, ".pdf"))
    {
        // TODO: pass format and actual key as separate parameters.
        // Hacking it out from a filename is bad ju-ju.
        $key = substr($key, 0, strlen($key)-4);
        $format = 1;
        if (strstr($key, "-")) {
            $list = array();
            $list = explode("-", $key);
            $key = $list[0];
            $format = $list[1];
        }

        $db = getDBObject();
        if (!$db->updateBookCounter($key, $format))
            error_log("FB2PDF ERROR. Unable to update book's counter. Key=$key"); 
    }
    
    httpRedirect($url);
}

?>