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

convTime = {};
totalConverted = 0;
totalTime = 0;

function process()
{
    convert();
    checkStatus();
    
    if (!endProcess())
        setTimeout('process()', 5000);
}

function endProcess()
{
    // check if there are still not finished items 
    for (var url in toConvert)
    {
        return false;
    }

    // display text
    document.getElementById('progress').style.display = 'none';
    document.getElementById('done').style.display = 'block';
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
            convTime[url] = new Date().getTime();
            
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
    
    var response = eval("(" + o.responseText + ")");
    
    toConvert[url] = response.key;
    
    // display book
    document.getElementById(url).style.display = ''
    
    var id = url + "_title";
    document.getElementById(id).innerHTML = response.author + ' "' + response.title + '" ';
    
    var id = url + "_status";
    document.getElementById(id).innerHTML = "Конвертируется...";
}

function convertFailureHandler(o)
{
    var url = o.argument.url;
    
    delete toConvert[url];
    delete convTime[url];
    
    // display error
    document.getElementById(url).style.display = ''
    
    var id = url + "_title";
    document.getElementById(id).innerHTML = o.statusText;
}

function statusSuccessHandler(o)
{
    var url = o.argument.url;
    
    var response = eval("(" + o.responseText + ")");
    
    // display status
    if (response.status == 'r')
    {
        // time of conversion
        totalConverted++;
        totalTime += (new Date().getTime() - convTime[url]);
        
        delete toConvert[url];
        delete convTime[url];
        
        var id = url + "_status";
        document.getElementById(id).innerHTML = 
            'Книга сконвертирована. ' +
            '<b><a href="' + response.converted + '">Загрузить книгу.</a></b> ' +
            '<a href="' + response.log + '">Посмотреть</a> возможные ошибки и предупреждения конвертации.';
    
        updateEstimatedTime();
    
    }
    else if (response.status == 'e')
    {
        delete toConvert[url];
        delete convTime[url];
        
        var id = url + "_status";
        document.getElementById(id).innerHTML = 
            'Ошибка конвертации. ' +
            '<a href="' + response.log + '">Посмотреть</a> ошибки конвертации.';
    }
}

function statusFailureHandler(o)
{
    var url = o.argument.url;
    delete toConvert[url];
    delete convTime[url];
    
    // display error
    var id = url + "_status";
    document.getElementById(id).innerHTML = 'Ошибка конвертации. ' + o.statusText;
}

function updateEstimatedTime()
{
    if (totalConverted > 0)
    {
        t = totalTime / totalConverted;
        document.getElementById("estimated_time").innerHTML = Math.ceil(t / (1000 * 60)) + " минут."
    }
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
                <p align="justify" class="small">Конвертация Ваших книг может занять некоторое время. Пожалуйста, не закрывайте окно Вашего браузера пока все книги не будут сконвертированны. В противном случае, часть книг может не сконвертироваться.</p>
                <p class="center"><span class="small">Приблизительное время ожидания: <span id="estimated_time">пока неизвестно</span></span></p>
                <p class="center"><img src="images/progress_conv.gif"/></p>
            </div>
            <div id="done" class="message" style="display:none">
                <h3>Конвертация Ваших книг закончена.</h3>
                <p align="justify" class="small">Теперь Вы можете загрузить сконветрированные книги и записать их в Ваш Sony Reader.
            </div>
            
            <div>
                <?php
                foreach ($sources as $source)
                {
                    $url = $source->getAttribute('url');
                    $bookId   = $url;
                    $titleId  = $url . "_title";
                    $statusId = $url . "_status";
                    
                    echo "<div id='$bookId' style='display: none'>
                            <span id='$titleId'></span>&nbsp;&nbsp;&nbsp;
                            <span id='$statusId'></span>
                          </div>";
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