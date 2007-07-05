<?php
	require_once "awscfg.php";
	require_once "db.php";
	require_once "utils.php";
	
	$current_url = getFullUrl("atom.php");
	//Normally I would indent and put propper spacing, but it doesn't work any other way
	echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>
<feed xmlns=\"http://www.w3.org/2005/Atom\">
<link rel=\"self\" href=\"$current_url\"/> 

	<title>Книги, сконвертированные недавно</title>
	<link href=\"http://codeminders.com/fb2pdf/staging/\"/>
	<id>urn:uuid:60a76c80</id>
	<updated>".date("Y\-m\-d\TH\:i\:s\Z")."</updated>
	";
	$limit = (isset($_GET["limit"])) ? $_GET["limit"] : 15;
	
	$db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
	$list = (isset($_GET["author"])) ? $db->getBooksByParcialAuthor($_GET["author"], $limit) : $db->getBooks($limit);
	
	for ($i = 0; $i < $limit; $i++)
	{
		$title   =    $list[$i]["title"];
		$author  =    $list[$i]["author"];
		$id      =    $list[$i]["id"];
		$date    =    formatDateIntoAtom($list[$i]["converted"]);
		$key     =    "getfile.php?key=" . $list[$i]["storage_key"]."";
		echo "
		<entry>
			<title>$title</title>
			<link href=\"$key\"/>
			<author>
				<name>$author</name>
			</author>
			<id>urn:uuid:$id</id>
			<updated>$date</updated>
			<summary>$author</summary>
		</entry>
		";
	}
	echo"
	</feed>
	";
?>