<?php
require_once "../www/awscfg.php";

$con = mysql_connect($dbServer, $dbUser, $dbPassword);

mysql_select_db($dbName, $con);
$set = @mysql_query ('SET NAMES UTF8');
$set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');


$result = mysql_query("SELECT * FROM OriginalBooks");

while($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
    $id    = $row["id"];
    $title = $row["title"];
    mysql_query("INSERT INTO TitleSearch (book_id, title) VALUES ('$id', '$title')");
}
echo "done";
?> 
