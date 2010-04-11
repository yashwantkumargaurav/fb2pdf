<?php
if (!isset ($_GET["author"]))
{
    header("HTTP/1.0 400 Bad Request");
    header('Content-type: text/html');    
    echo "<html><body>Missing \"author\" paremeter</body></html>";
    die;
}
$author = $_GET["author"];
$base    =  "atom.php";
$link    =  (isset($author)) ? "$base?author=$author" : $base;
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="alternate" type="application/atom+xml" title="Atom" href="<?php echo $link; ?>" />
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<?php include 'searchstyle.inc.php'; ?>
<?php include 'analytics.inc.php'; ?>
<?php include 'searchstyle.inc.php'; ?>
</head>

<body>
<center>
<div id="container" class="WidthPage">
    <?php 
    include 'header.inc.php'; 
    $active_menu = 'books';
    include 'menu.inc.php'; 
    ?>

    <div id="tab_box">
        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
        <div class="tab_box_content">
        
            <?php
            require_once 'awscfg.php';
            require_once 'db.php';
            require_once 'utils.php';

            global $awsS3Bucket;
            global $dbServer, $dbName, $dbUser, $dbPassword;
                
            $db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
            $list = $db->getBooksByAuthor($author, 0);
            if ($list)
            {
                echo "<div class=\"author\"><br/>$author</div>";
                //echo "<img src=\"images/lg_px.gif\" class=\"line\"/>";
                echo "<img src=\"images/green_px.gif\" class=\"line\"/>";
                
                $count = count($list);
                
                $MAX_COLS  = 2;
                $MAX_ROWS  = floor(($count + $MAX_COLS - 1) / $MAX_COLS);
                
                for ($col = $MAX_COLS - 1; $col >= 0 ; $col--)
                {
                    if ($col == 0)
                        echo '<div class="left_book">';
                    else
                        echo '<div class="right_book">';
                    
                    for ($row = 0; $row < $MAX_ROWS; $row++)
                    {
                        $i = $col * $MAX_ROWS + $row;
                        echo "<p>";
                        if ($i < $count)
                        {
                            $title  = $list[$i]["title"];
                            $key    = $list[$i]["storage_key"];

                            if (!$title)
                                $title = "Название неизвестно";
                            
                            echo "<a href=\"book.php?key=$key\">\"$title\"</a><br/>";
                        }
                        echo "</p>";
                    }
                    echo '</div>';
                }
                
                //echo "<img src=\"images/lg_px.gif\" class=\"line\"/>";
                echo "<img src=\"images/green_px.gif\" class=\"line\"/>";
            }
            ?>
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
