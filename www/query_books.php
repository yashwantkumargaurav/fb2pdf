<?php

require_once 'awscfg.php';
require_once 'db.php';

global $awsS3Bucket;
global $dbServer, $dbName, $dbUser, $dbPassword;

$author = (isset($_GET["author"])) ? $_GET["author"] : NULL;
$count  = (isset($_GET["count"]))  ? $_GET["count"]  : 0;

if (!$author || !is_numeric($count))
{
    header("HTTP/1.0 400 Bad Request");
    header('Content-type: text/html');    
    if (!$author)
        echo "<html><body>Missing \"author\" parameter</body></html>";
    else
        echo "<html><body>Parameter \"count\" must be a number</body></html>";
    die;
}

$db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
$list = $db->getBooksByAuthor($author, $count);
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
echo "<title>$author</title>";

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