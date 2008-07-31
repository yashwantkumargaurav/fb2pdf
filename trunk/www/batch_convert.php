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
    
    if (!endProcess())
        setTimeout('process()', 5000);
}

function endProcess()
{
    // check if there are still not finished items 
    for (var url in toConvert)
        return false;

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
            
            // callback
            var callback =
            {
                success: convertSuccessHandler,
                failure: convertFailureHandler,
                argument: { url: url }
            };
            
            // Initiate the HTTP GET request.
            var request = YAHOO.util.Connect.asyncRequest('GET', requestUrl, callback);
            
            // display status
            var id = url + "_status";
            document.getElementById(id).innerHTML = "Загружается...";
            
            break;
        }
    }
}

function checkStatus()
{
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
    var id = url + "_author";
    document.getElementById(id).innerHTML = response.author;
    
    var id = url + "_title";
    document.getElementById(id).innerHTML = '"' + response.title + '"';
    
    var id = url + "_status";
    document.getElementById(id).innerHTML = "Конвертируется...";
}

function convertFailureHandler(o)
{
    var url = o.argument.url;
    
    delete toConvert[url];
    totalConverted++;
    updateProgress();
    
    // display error
    var id = url + "_status";
    document.getElementById(id).innerHTML = "Ошибка загрузки <a href='" + url + "' target='_blank'>файлa</a>.";
}

function statusSuccessHandler(o)
{
    var url = o.argument.url;
    
    var response = eval("(" + o.responseText + ")");
    
    // display status
    if (response.status == 'r')
    {
        delete toConvert[url];
        totalConverted++;
        updateProgress();
        
        var id = url + "_title";
        var title = document.getElementById(id).innerHTML;
        document.getElementById(id).innerHTML = "<a href='" + response.converted + "'>" + title + "</a>";

        var id = url + "_status";
        document.getElementById(id).innerHTML = "Книга сконвертирована. " +
            "<b><a href='" + response.converted + "'>Загрузить.</a></b>";
    }
    else if (response.status == 'e')
    {
        delete toConvert[url];
        totalConverted++;
        updateProgress();
        
        var id = url + "_status";
        document.getElementById(id).innerHTML = "Ошибка конвертации. " +
            "<a href='" + response.log + "' target='_blank'>Посмотреть.</a>";
    }
}

function statusFailureHandler(o)
{
    var url = o.argument.url;
    
    delete toConvert[url];
    totalConverted++;
    updateProgress();
    
    // display error
    var id = url + "_status";
    document.getElementById(id).innerHTML = "Ошибка конвертации.";
}

function updateProgress()
{
    if (totalConverted > 0 && totalFiles > 0)
    {
        document.getElementById("percentage").innerHTML = Math.ceil(totalConverted * 100 / totalFiles) + "%";
        
        document.getElementById("converted_books").innerHTML = totalConverted;
        document.getElementById("total_books").innerHTML = totalFiles;
    }
}
</script>

<?php
require_once 'utils.php';

// Parse POSTED data
$MAX_BOOKS = 20;
$sources = array();
for ($i = 0; $i < $MAX_BOOKS; $i++)
{
    $name = 'book' . $i;
    if (isset($_POST[$name]))
        $sources[] = $_POST[$name];
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
                <p align="center" class="small">Сконвертировано книг: <span id="converted_books">0</span> из <span id="total_books">0</span>.</p>
                <p class="center"><img src="images/progress_conv.gif"/>&nbsp;&nbsp;<span id="percentage">0%</span></p>
            </div>
            <div id="done" class="message" style="display:none">
                <h3>Конвертация Ваших книг закончена.</h3>
                <p align="justify" class="small">Теперь Вы можете загрузить сконвертированные книги и записать их в Ваш Sony Reader.
            </div>
            
            <div class="right_book">
                <?php
                foreach ($sources as $url)
                {
                    $statusId = $url . "_status";
                    echo "<span id='$statusId'></span><br/><br/>";
                }
                ?>
            </div>
            
            <div class="left_book">
                <?php
                $n = 1;
                foreach ($sources as $url)
                {
                    $authorId = $url . "_author";
                    $titleId  = $url . "_title";
                    echo "<span id='$authorId'>Книга $n</span>&nbsp;&nbsp;<span id='$titleId'></span><br/><br/>";
                    $n++;
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
var toConvert      = {};
var totalFiles     = 0;
var totalConverted = 0;

<?php
$count = count($sources);    
echo "totalFiles = $count;";

foreach ($sources as $url)
    echo "toConvert[\"$url\"] = null;";
?>

process();
</script>

</body>
</html>