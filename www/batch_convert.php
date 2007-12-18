<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="alternate" type="application/atom+xml" title="Atom" href="atom.php" />
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<?php include 'analytics.inc.php'; ?>

<script src="js/yahoo.js"></script>
<script src="js/connection.js"></script>

<script type="text/javascript">
function process()
{
    convert();
    checkStatus();
    
    // check if there are still not finished items 
    var allDone = true;
    for (var url in toConvert)
    {
        if (toConvert[url] == null || toConvert[url])
            allDone = false;
    }
    if (!allDone)
        setTimeout('process()', 5000);
    else
        alert ("All Done");
}

function convert()
{
    for (var url in toConvert)
    {
        // find the first book which is not converted yet
        if (toConvert[url] == null)
        {
            var requestUrl = encodeURI('conv_process.php?url=' + url);

            toConvert[url] = 0;
            
            // callback
            var callback =
            {
                success: convertSuccessHandler,
                failure: convertFailureHandler,
                argument: { url: url }
            };
            
            // Initiate the HTTP GET request.
            var request = YAHOO.util.Connect.asyncRequest('GET', requestUrl, callback);
            break;
        }
    }
}

function checkStatus()
{
    var convList = new Array();
    for (var url in toConvert)
    {
        if (toConvert[url])
        {
            var requestUrl = encodeURI('conv_status.php?key=' + toConvert[url]);

            // callback
            var callback =
            {
                success: statusSuccessHandler,
                failure: statusFailureHandler,
                argument: { url: url }
            };
            
            // Initiate the HTTP GET request.
            var request = YAHOO.util.Connect.asyncRequest('GET', requestUrl, callback);
        }
    }
}

function convertSuccessHandler(o)
{
    var url = o.argument.url;
    
    // format and display results.
    var root = o.responseXML.documentElement;
    
    var key    = root.getElementsByTagName("key")[0].firstChild.nodeValue;
    var author = root.getElementsByTagName("author")[0].firstChild.nodeValue;
    var title  = root.getElementsByTagName("title")[0].firstChild.nodeValue;

    toConvert[url] = key;
    displayStatus(url, "converting...");
}

function convertFailureHandler(o)
{
    var url = o.argument.url;
    toConvert[url] = 0;
    displayStatus(url, "error: (" + o.status + " " + o.statusText + ")");
}

function statusSuccessHandler(o)
{
    var url = o.argument.url;
    
    // format and display results.
    var root = o.responseXML.documentElement;
    
    var status = root.getElementsByTagName("status")[0].firstChild.nodeValue;
    var source = root.getElementsByTagName("source")[0].firstChild.nodeValue;
    if (status == 'r' || status == 'e')
    {
        toConvert[url] = 0;
        
        var converted = root.getElementsByTagName("converted")[0].firstChild.nodeValue;
        var log = root.getElementsByTagName("log")[0].firstChild.nodeValue;
        
        displayStatus(url, "status = " + status + " source = " + source + " converted = " + converted + " log = " + log);
    }
    else
    {
        displayStatus(url, "converting...");
    }
}

function statusFailureHandler(o)
{
    var url = o.argument.url;
    toConvert[url] = 0;
    displayStatus(url, "error: (" + o.status + " " + o.statusText + ")");
}

function displayStatus(url, test)
{
    document.getElementById(url).innerHTML = url + " - " + test;
}

</script>

<?php
require_once 'utils.php';

// Parse POSTED data
$dom = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST')
{
    $postText = trim(file_get_contents('php://input'));
    $dom = DOMDocument::loadXML($postText);
}

if ($dom)
{
    $sources = $dom->getElementsByTagName('source');
}
else
{
    httpResponseCode("400 Bad Request", "Wrong or missing XML has been posted");
    die;
}
?>

</head>

<body>
<center>
<div id="container" class="WidthPage">
    <?php 
    include 'header.inc.php'; 
    $active_menu = 'status';
    include 'menu.inc.php'; 
    ?>
    
    <div id="tab_box">
        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
        <div class="tab_box_content">
            <img src="images/green_px.gif" class="line"/>
            
            <div id="progress" class="message" style="display:block">
                <p align="justify" class="small">Конвертация Вашего книг может занять некоторое время. Пожалуйста, не закрывайте окно Вашего браузера пока все книги не будут сконвертированны. В противном случае, часть книг может не сконвертироваться.</p>
                <p class="center"><span class="small">Приблизительное время ожидания: <span id="estimated_time">пока неизвестно</span></span></p>
                <p class="center"><img src="images/progress_conv.gif"/></p>
            </div>
            
            <div id="converted">
                <?php
                foreach ($sources as $source)
                {
                    $url  = $source->getAttribute('url');
                    $name = $source->getAttribute('name');
                    
                    echo "<div id=\"$url\">$name</div>";
                }
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
            
            
<script type="text/javascript">
var toConvert = {};

<?php
foreach ($sources as $source)
{
    $url  = $source->getAttribute('url');
    echo "toConvert[\"$url\"] = null;";
}
?>

process();
</script>

</body>
</html>