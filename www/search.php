<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<?php include 'searchstyle.inc.php'; ?>
<?php include 'analytics.inc.php'; ?>
</head>

<body>
<center>
<div id="container" class="WidthPage">
    <?php 
    include 'header.inc.php'; 
    $active_menu = '';
    include 'menu.inc.php'; 
    ?>
    
    <div id="tab_box">
        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
        <div class="tab_box_content">
            <img src="images/green_px.gif" class="line"/>
            <p>
            <?php
            require_once 'awscfg.php';
            require_once 'db.php';
            require_once 'utils.php';
    
            global $awsS3Bucket;
            global $dbServer, $dbName, $dbUser, $dbPassword;
                
            $db = new DB($dbServer, $dbName, $dbUser, $dbPassword);

            //Page numbers for author & title
            $page_title  = (isset($_GET["page_t"])) ? $_GET["page_t"] : 1;
            $page_author = (isset($_GET["page_a"])) ? $_GET["page_a"] : 1;
            
            $per_page = 10;

            $countTitles  = $db->countTitles($_GET["search"]);
            $countAuthors = $db->countAuthors($_GET["search"]);

            //Max page numbers for each
            $total_title_pages  = floor($countTitles  / 10) + (($countTitles  % $per_page == 0) ? 0 : 1);
            $total_author_pages = floor($countAuthors / 10) + (($countAuthors % $per_page == 0) ? 0 : 1);

            //For page changing
            $url = $_SERVER["PHP_SELF"] . "?search=" . $_GET["search"];

            if ($total_title_pages != 0) {
                $title  = $db->searchTitles($_GET["search"], ($page_title - 1) * $per_page, $page_title * $per_page);
                echo 'Books:
                      <br/>
                      <img src="images/green_px.gif" class="line"/> <br/>';
            
                $limit = ($countTitles < $per_page) ? $countTitles : $per_page;
                for ($i = 0; $i < $limit; $i++)
                    echo '<a href="book.php?key=' . $title[$i]["storage_key"] . '">' . $title[$i]['title'] . '</a>
                          <br/>
                          By: ' . $title[$i]["author"] . ' <br/><br/>';

                //Show pages switch if there are more than 1 page
                if ($total_title_pages > 1) {
                    echo '<br/>';      
                    
                    //Prev
                    if ($page_title != 1)              
                        echo '<a href="'. $url .'&page_t='. ($page_title - 1) .'"><< Prev</a> ';

                    //Page numbers
                    for ($i = 1; $i < $total_title_pages + 1; $i++) {
                        if ($i == $page_title)
                            echo '<b>'. $i .'</b> ';
                        else
                            echo '<a href="'. $url .'&page_a='. $i .'">'. $i .'</a> ';
                    }

                    //Next
                    if ($page_title != $total_title_pages)
                        echo '<a href="'. $url .'&page_t='. ($page_title + 1) .'">Next >></a>';
                }

            }
            if ($total_author_pages != 0) {
                $author = $db->searchAuthors($_GET["search"], ($page_author - 1) * $per_page, $page_author * $per_page);
                echo '<img src="images/green_px.gif" class="line"/> <br/>
                      Authors:
                      <br/>
                      <img src="images/green_px.gif" class="line"/> <br/>';

                $limit = ($countAuthors < $per_page) ? $countAuthors : $per_page;
                for ($i = 0; $i < $limit; $i++)
                    echo '<a href="books.php?author=' . $author[$i]['author'] . '">' . $author[$i]['author'] . '</a><br/>';            

                if ($total_author_pages > 1) {
                    echo '<br/>';

                    //Prev
                    if ($page_author != 1)
                        echo '<a href="'. $url .'&page_a='. ($page_author - 1) .'"><< Prev</a> ';

                    //Page numbers
                    for ($i = 1; $i < $total_author_pages + 1; $i++) {
                        if ($i == $page_author)
                            echo '<b>'. $i .'</b> ';
                        else
                            echo '<a href="'. $url .'&page_a='. $i .'">'. $i .'</a> ';
                    }

                    //Next
                    if ($page_author != $total_author_pages)
                        echo '<a href="'. $url .'&page_a='. ($page_author + 1) .'">Next >></a>';
                }  

            }

            if (count($author) == 0 && count($title) == 0)
                echo 'No results found';
            ?>
            </p>
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
