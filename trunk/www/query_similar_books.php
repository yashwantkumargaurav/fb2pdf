<?php

require_once 'awscfg.php';
require_once 'db.php';

global $awsS3Bucket;
global $dbServer, $dbName, $dbUser, $dbPassword;

$excludeKey = (isset($_GET["excludedKey"])) ? $_GET["excludedKey"] : NULL;
$group = (isset($_GET["group"])) ? $_GET["group"] : 0;
$count  = (isset($_GET["count"]))  ? $_GET["count"]  : 0;

if (!is_numeric($group) || !is_numeric($count) || !$excludeKey)
{
    header("HTTP/1.0 400 Bad Request");
    header('Content-type: text/html');  
    if (!$excludeKey) 
    	echo "<html><body>Missing \"excludedKey\" parameter</body></html>";
    else if (!is_numeric($group))
        echo "<html><body>Parameter \"group\" must be a number</body></html>";
    else
        echo "<html><body>Parameter \"count\" must be a number</body></html>";
    die;
}

$db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
$list = $db->getBooksByGroup($group, $excludeKey, $count);
if ($list === false)
{
    header("HTTP/1.0 500 Internal Server Error");
    header('Content-type: text/html');    
    echo "<html><body>Internal Error</body></html>";
    die;
}

header('HTTP/1.0 200 OK');
header('Content-type: text/xml');    

// generate rss xml
echo '<?xml version="1.0" encoding="UTF-8"?>';
echo '<rss version="2.0">';
echo '<channel>';
echo "<title>$group</title>";

for ($i = 0; $i < count($list); $i++)
{
    $title  = $list[$i]["title"];
    $key    = $list[$i]["storage_key"];

    if (!$title)
        $title = "Название неизвестно";
    
    echo '<item>';
    echo "<title>$title</title>";
    echo "<link>book.php?key=$key</link>";
    echo '</item>';
}

echo '</channel>';
echo '</rss>';

?>