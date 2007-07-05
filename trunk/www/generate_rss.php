<?php
	require_once "awscfg.php";
	require_once "db.php";
	//Normall I would indent and put propper spacing, but it doesn't work any other way
	echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>
<feed xmlns=\"http://www.w3.org/2005/Atom\">

	<title>Книги, сконвертированные недавно</title>
	<link href=\"http://codeminders.com/fb2pdf/staging/\"/>
	<id>urn:uuid:60a76c80</id>
	";
	$limit = (isset($_GET["limit"])) ? $_GET["limit"] : 15;
	
	$db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
	$list = (isset($_GET["author"])) ? $db->getBooksByParcialAuthor($_GET["author"], $limit) : $db->getBooks($limit);
	
	for ($i = 0; $i < $limit; $i++)
	{
		$title   =    $list[$i]["title"];
		$author  =    $list[$i]["author"];
		$id      =    $list[$i]["id"];
		$key     =    "getfile.php?key=" . $list[$i]["storage_key"]."";
		echo "
		<entry>
			<title>$title</title>
			<link href=\"$key\"/>
			<author>$author</author>
			<id>urn:uuid:$id</id>
			<summary>$author</summary>
		</entry>
		";
	}
	echo"
	</feed>
	";
?>