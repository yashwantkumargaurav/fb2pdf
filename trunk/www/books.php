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
<script src="js/yahoo.js"></script>
<script src="js/connection.js"></script>

<script type="text/javascript">
function bookTitles(groupId, totalNumber, excludedKey, divName, imgName)
{
    if ( document.getElementById(divName).style.display == 'none') 
    {
        // show progress indicator
        var div = document.getElementById(divName);
        div.innerHTML = '<img id="pimage" src="images/progress.gif" alt="progress bar"/>';
        div.style.display="inline";
        
        // request url 
        var baseUrl = 'query_similar_books.php';
        var queryString = encodeURI('?group=' + groupId + '&' + 'count=' + 0 + '&' + 'excludedKey=' + excludedKey);
        var url = baseUrl + queryString;

        // callback
        var callback =
        {
            success: successHandler,
            failure: failureHandler,
            argument: { divName: divName, imgName: imgName, groupId: groupId, totalNumber: totalNumber }
        };
        
        // Initiate the HTTP GET request.
        var request = YAHOO.util.Connect.asyncRequest('GET', url, callback);
    }   
    else
    {
        document.getElementById(divName).style.display="none";
        document.getElementById(imgName).src = document.getElementById(imgName).src.replace('_minus', '_plus');
    }
}

function successHandler(o)
{
    var div = document.getElementById(o.argument.divName);
    var img = document.getElementById(o.argument.imgName);
    var groupId = o.argument.groupId;
    var totalNumber = o.argument.totalNumber;
    
    // format and display results.
    var root = o.responseXML.documentElement;
    var channel = root.getElementsByTagName("channel")[0];
    
    var items = channel.getElementsByTagName("item");
    
    div.innerHTML = '';
    for (var i = 0; i < items.length; i++)
    {
        var title = items[i].getElementsByTagName("title")[0].firstChild.nodeValue;
        var link  = items[i].getElementsByTagName("link")[0].firstChild.nodeValue;
        
        div.innerHTML +=  '<a href="' + link + '">' + title + '</a><br>';
    }

    // display list
    div.style.display = "inline";
    img.src = img.src.replace('_plus', '_minus');
}

function failureHandler(o)
{
    alert("Внутренняя ошибка системы (" + o.status + " " + o.statusText + ")");
    
    var div = document.getElementById(o.argument.divName);
    var img = document.getElementById(o.argument.imgName);
    
    div.innerHTML = '';
    div.style.display = "none";
    img.src = img.src.replace('_minus', '_plus');
}

function rollOver(imgName)
{
    if (document.getElementById(imgName).src.search('_off') > 0)
    {
        document.getElementById(imgName).src = document.getElementById(imgName).src.replace('_off', '_on');
    }
    else
    {
        document.getElementById(imgName).src = document.getElementById(imgName).src.replace('_on', '_off');
    }
}
</script>
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
                            
                            if($list[$i]["group"]){
                            	$title_md5 = md5($title);
                            	$groupId = $list[$i]["group"];
                            	echo "<img id=\"bt$title_md5\" src=\"images/bt_plus_off.gif\" style=\"cursor:pointer\"";
	                            echo " onclick=\"bookTitles('$groupId', 0, '$key', '$title_md5', 'bt$title_md5');\"";
	                            echo " onmouseover=\"rollOver('bt$title_md5');\"";
	                            echo " onmouseout=\"rollOver('bt$title_md5');\"/>";
	                            echo "&nbsp;&nbsp;<a href=\"book.php?key=$key\">\"$title\"</a>&nbsp;&nbsp;<br/>"; 
	                            echo "<div id=\"$title_md5\" style=\"display:none;\">";
	                            echo "</div>";
                            }
                            else{
                            	echo "<a href=\"book.php?key=$key\">\"$title\"</a><br/>";
                            }
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
