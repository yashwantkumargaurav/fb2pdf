<?php
require_once 'utils.php';
require_once 'db.php';
require_once 'process.php';

if (!isset ($_GET['key']))
{
    httpResponseCode("400 Bad Request", "Missing parameter \"key\"");
    die;
}
$key = removeExt($_GET['key']);

$bs = new BookStatus();
try
{
    $bs->checkOriginal($key);
    
    // get book info
    $db = getDBObject();
    $bookInfo = $db->getBookByKey($key);

    $id     = $bookInfo["id"];
    $title  = $bookInfo["title"];
    $author = $bookInfo["author"];

    if (!$author)
        $author = "Автор неизвестен";
    if (!$title)
        $title = "Название неизвестно";

    $formats = $db->getFormats();
}
catch(Exception $e)
{
    error_log("FB2PDF ERROR. Status: " . $e->getMessage()); 
    httpResponseCode("400 Bad Request", $e->getMessage());
}
    
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="alternate" type="application/atom+xml" title="Atom" href="atom.php" />
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<?php include 'analytics.inc.php'; ?>
</head>

<body>
<center>
<div id="container" class="WidthPage">
    <?php 
    include 'header.inc.php'; 
    $active_menu = 'book';
    include 'menu.inc.php'; 
    ?>

    <div id="tab_box">
        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
        <div class="tab_box_content">
            <img src="images/green_px.gif" class="line"/>
            <div id="status" class="message">
                <?php        
                    echo "<h3 class='left'><a href='books.php?author=$author' style='color:black'>$author</a>&nbsp;&nbsp;\"$title\"</h3><br/><br/>";
                    echo "<p>Загрузить книгу в формате:<br/>";
                    echo "[<a href='$bs->fbFile'>оригинал (fb2)</a>]<br/>";
                    if ($formats) {
                        $count = count($formats);
                        for ($i = 0; $i < $count ; $i++)
                        {
                            $format = $formats[$i]["id"];
                            $formatTitle = $formats[$i]["title"];
                            $status = $bs->checkConverted($key, $format);
                            if ($status == BookStatus::STATUS_SUCCESS)
                            {
                                echo "[<a href='$bs->pdfFile'>$formatTitle (pdf)</a>]<br/>";
                            }
                            else {
                                echo "[<a href='convert.php?key=$key&format=$format'>$formatTitle (pdf)</a>]<br/>";
                            }
                        }
                    }
                    echo "<p><a href='books.php?author=$author' style='color:black'>Другие книги автора</a></p>";
                    echo "<p>";
                    $book_link  = getFullUrl("book.php") . "?key=".urlencode($key);
                    $book_path  = "/book/".$key;
                    $book_title = $author."  '".$title."'";
                    echo "<div class=\"js-kit-rating\" title=\"$book_title\" permalink=\"$book_link\" path=\"$book_path\"></div>";
                    echo "<div class=\"js-kit-comments\" permalink=\"$book_link\" path=\"$book_path\"></div>";
                    echo "<script src=\"http://js-kit.com/reviews.js\" permalink=\"$book_link\" path=\"$book_path\"></script>";
                ?>
            </div>    
            <img src="images/green_px.gif" class="line"/>
            <?php include 'footer.inc.php'; ?>
        </div>  <!--end of tab box content-->	
        <b class="xbottom"><b class="xb4"></b><b class="xb3"></b><b class="xb2"></b><b class="xb1"></b></b>
    </div> <!--end of tab box -->
<br/>
<br/>
</div> <!--end of container-->
    
</center>
</body>
</html>
