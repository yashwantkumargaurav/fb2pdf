<?php
	require_once "awscfg.php";
	require_once "db.php";
	require_once "utils.php";
	
	$current_url  =     getFullUrl("atom.php");
	$db           =     new DB($dbServer, $dbName, $dbUser, $dbPassword);
	$limit        =    (isset($_GET["limit"]))  ? $_GET["limit"] : 15;
	$list         =    (isset($_GET["author"])) ? $db->getBooksByParcialAuthor($_GET["author"], $limit)  :   $db->getBooks($limit);
	
    $last_modified = date(DATE_RFC822, strtotime($list[0]["converted"]));
    
    header("Content-Type: application/atom+xml; charset=utf-8"); 
	header("Last-Modified: ". $last_modified);
	
	
	echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>
	<feed xmlns=\"http://www.w3.org/2005/Atom\">
	<link rel=\"self\" href=\"$current_url\"/> 
	";

    if (isset($_GET["author"]))
    {
        $byauthor = $_GET["author"];
        echo "<title>FB2PDF. Новые книги $byauthor.</title>";
    }
    else
        echo "<title>FB2PDF. Новые книги.</title>";
    
	echo "<link href=\"http://fb2pdf.com/\"/>
	<id>urn:uuid:60a76c80</id>
	<updated>".date("Y\-m\-d\TH\:i\:s\Z")."</updated>
	";
	
	if ($limit > count($list))
		$limit = count($list);
	
	for ($i = 0; $i < $limit; $i++)
	{
		$title   =    $list[$i]["title"];
		$author  =    $list[$i]["author"];
		$id      =    $list[$i]["id"];
		$date    =    formatDateIntoAtom($list[$i]["converted"]);
		$key     =    "getfile.php?key=" . $list[$i]["storage_key"]."";
		if (!$author)
			$author = "Автор неизвестен";
		if (!$title)
			$title = "Название неизвестно";
		echo "
		<entry>
			<title>$author. $title</title>
			<link href=\"$key\"/>
			<author>
				<name>$author</name>
			</author>
			<id>urn:uuid:$id</id>
			<updated>$date</updated>	
			<content type=\"html\">&lt;a href=\"$key\"&gt;$author. $title&lt;/a&gt;</content>
		</entry>
		";
	}
	echo "
	</feed>
	";
?>