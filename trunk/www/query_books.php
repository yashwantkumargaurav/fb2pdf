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
        echo "<html><body>Missing \"author\" paremeter</body></html>";
    else if (!is_numeric($count))
        echo "<html><body>The \"count\" paremeter must be a number</body></html>";
    die;
}

header('HTTP/1.0 200 OK');
header('Content-type: text/xml');    

$db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
$list = $db->getBooksByAuthor($author, $count);

// generate rss xml
echo '<?xml version="1.0" encoding="UTF-8"?>';
echo '<rss version="2.0">';
echo '<channel>';
echo "<title>$author</title>";

for ($i = 0; $i < count($list); $i++)
{
    $title  = $list[$i]["title"];
    $key    = $list[$i]["storage_key"];
    if (strrpos($key, ".") === false) // old style key (no extension)
        $key = $key . ".pdf";

    if (!$title)
        $title = "Название неизвестно";
    
    echo '<item>';
    echo "<title>$title</title>";
    echo "<link>getfile.php?key=$key</link>";
    echo '</item>';
}

echo '</channel>';
echo '</rss>';

?>