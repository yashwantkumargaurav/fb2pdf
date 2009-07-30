<?php
require_once "../www/awscfg.php";

$con = mysql_connect($dbServer, $dbUser, $dbPassword);

mysql_select_db($dbName, $con);
$set = @mysql_query ('SET NAMES UTF8');
$set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');


$result = mysql_query("SELECT * FROM OriginalBooks");

while($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
    $author = $row["author"];
    mysql_query("INSERT INTO AuthorSearch (author) VALUES ('$author')");
}
echo "done";
?> 
