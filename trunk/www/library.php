<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="alternate" type="application/atom+xml" title="Atom" href="atom.php" />
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>

<script src="js/yahoo.js"></script>
<script src="js/connection.js"></script>

<script type="text/javascript">
//  Show/Hide 5 first titles
function bookTitles(author, totalNumber, divName, imgName)
{
    if ( document.getElementById(divName).style.display == 'none') 
    {
        // show progress indicator
        var div = document.getElementById(divName);
        div.innerHTML = '<img id="pimage" src="images/progress.gif" alt="progress bar"/>';
        div.style.display="inline";
        
        // request url 
        var baseUrl = 'query_books.php';
        var queryString = encodeURI('?author=' + author + '&' + 'count=' + 5);
        var url = baseUrl + queryString;

        // callback
        var callback =
        {
            success: successHandler,
            failure: failureHandler,
            argument: { divName: divName, imgName: imgName, author: author, totalNumber: totalNumber }
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
    var author = o.argument.author;
    var totalNumber = o.argument.totalNumber;
    
    // format and display results.
    var root = o.responseXML.documentElement;
    var channel = root.getElementsByTagName("channel")[0];
    
    //var author = channel.getElementsByTagName("title")[0].firstChild.nodeValue;
    
    var items = channel.getElementsByTagName("item");
    
    div.innerHTML = '';
    for (var i = 0; i < items.length; i++)
    {
        var title = items[i].getElementsByTagName("title")[0].firstChild.nodeValue;
        var link  = items[i].getElementsByTagName("link")[0].firstChild.nodeValue;
        
        div.innerHTML +=  '<a href="' + link + '">' + title + '</a><br>';
    }
    
    if (totalNumber > 5)
    {
        var queryString = encodeURI('?author=' + author);
        div.innerHTML += '<a href="books.php' + queryString + '"><i>Все книги автора...</i></a>';
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
    $active_menu = 'library';
    include 'menu.inc.php'; 
    ?>
    
    <div id="tab_box">
        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
        <div class="tab_box_content">
            <!--  display alphabet --> 
            <div id="alphabet">
                <?php
                require_once 'awscfg.php';
                require_once 'db.php';
                require_once 'utils.php';

                global $dbServer, $dbName, $dbUser, $dbPassword;

                $db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
                $dbLetters = $db->getAuthorsFirstLetters();

                $letter = isset($_GET["letter"]) ? strtoupper($_GET["letter"]) : "А";
                $alphabet = array(
                    array("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"),
                    array("А","Б","В","Г","Д","Е","Ё","Ж","З","И","Й","К","Л","М","Н","О","П","Р","С","Т","У","Ф","Х","Ц","Ч","Ш","Щ","Э","Ю","Я")
                    );

                for ($i = 0; $i < count($alphabet); $i++)
                {
                    $letters = $alphabet[$i];
                    foreach ($letters as $l)
                    {
                        if (in_array($l, $dbLetters))
                        {
                            if ($letter == $l)
                                echo "<span class=\"active\">$l</span> ";
                            else
                                echo "<a href=\"library.php?letter=$l\">$l</a> ";
                        }
                        else
                            echo "$l ";
                    }
                    echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                }
                ?>
            </div>
            <img src="images/green_px.gif" class="line"/>
            
            <!--  display authors --> 
            <?php
            $list = $db->getAuthorsByFirstLetter($letter);
            if ($list)
            {
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
                            $author = $list[$i]["author"];
                            $number = $list[$i]["number"];
                            
                            $author_md5 = md5($author);
                            
                            echo "<img id=\"bt$author_md5\" src=\"images/bt_plus_off.gif\" style=\"cursor:pointer\"";
                            echo " onclick=\"bookTitles('$author', $number, '$author_md5', 'bt$author_md5');\"";
                            echo " onmouseover=\"rollOver('bt$author_md5');\"";
                            echo " onmouseout=\"rollOver('bt$author_md5');\"/>";
                            echo "&nbsp;&nbsp;$author&nbsp;&nbsp;<br/>"; 
                            echo "<div id=\"$author_md5\" style=\"display:none;\">";
                            echo "</div>";
                        }
                        echo "</p>";
                    }
                    echo '</div>';
                }
            }
            ?>
            
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