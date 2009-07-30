<?php
header('Content-type: text/html; charset=utf-8');

if (strlen($_GET['query']) == 0)
    return;

require_once 'awscfg.php';
require_once 'db.php';
require_once 'utils.php';

global $awsS3Bucket;
global $dbServer, $dbName, $dbUser, $dbPassword;

$query = html_entity_decode(urldecode($_GET['query']));
    
$db = new DB($dbServer, $dbName, $dbUser, $dbPassword);

$tbl = array_merge($db->scoreTitle($query), $db->scoreAuthor($query));

if (count($tbl) == 0)
    return;

foreach ($tbl as $key => $row)
    $score[] = $row['score'];

array_multisort($score, SORT_DESC, $tbl);

for ($i = 0; $i < count($tbl); $i++)
	echo $tbl[$i]["text"]."\n";
?>
