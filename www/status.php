<?php
require_once 'db.php';
require_once 'utils.php';

if (!isset ($_GET['key']))
{
    httpResponseCode("400 Bad Request", "Missing parameter \"key\"");
    die;
}
$key = $_GET['key'];

// get book info
$db = getDBObject();
$bookInfo = $db->getBookByKey($key);

$book = "";
if ($bookInfo)
{
    $title  = $bookInfo["title"];
    $author = $bookInfo["author"];
    if ($title and $author)
        $book = "($author&nbsp;&nbsp;\"$title\")";
}
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="alternate" type="application/atom+xml" title="Atom" href="atom.php" />
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<?php include 'searchstyle.inc.php'; ?>
<?php include 'analytics.inc.php'; ?>


</head>
<body>


<div id="survey-prompt" style="background-color:white;z-index:99999;padding:2;position:absolute;top:20px;left:5px;width:275px">


Мы проводим небольшой опрос пользователей, чтобы
решить как мы можем улучшить сайт. Мы будем
благодарны если вы потратите пару минут вашего
времени чтобы ответить на несколько вопросов.
<br><br>
<b><a href="http://www.surveymonkey.com/s.aspx?sm=TNNb2tslWSrdK6TvgPa_2fsA_3d_3d" target="_blank">[Принять участие в опросе]</a></b>
<i>(опрос отроется в новом окне броузера)</i>.
<br>
<script type="text/javascript">
function hideSurveyPrompt()
{
    document.getElementById("survey-prompt").style.display="none";
}

</script>
<a href="javascript:hideSurveyPrompt()">[спрятать]</a>
</div>

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
            <img src="images/lg_px.gif" class="line"/>
            <div id="status" class="message">
                <h3 class="left">Конвертация книги <?php echo $book; ?> может занять несколько минут. Пожалуйста, подождите...</h3>
                <p class="center"><img src="images/progress_conv.gif"/></p>
                <p>Эта страница обновится автоматически, когда процесс конвертации будет закончен. 
                Вы можете также сохранить URL этой страницы и вернуться к ней в любое удобное для Вас время, 
                чтобы забрать готовый сконвертированный файл.</p>
                <p><a href="index.php">Сконвертировать ещё одну книгу.</a><br/></p>
            </div>    
            <img src="images/lg_px.gif" class="line"/>
            <?php include 'footer.inc.php'; ?>
        </div>  <!--end of tab box content-->	
        <b class="xbottom"><b class="xb4"></b><b class="xb3"></b><b class="xb2"></b><b class="xb1"></b></b>
    </div> <!--end of tab box -->
<br/>
<br/>
</div> <!--end of container-->
</center>

<script src="js/yahoo.js"></script>
<script src="js/connection.js"></script>

<script type="text/javascript">

<?php
echo "var key = '$key';";
echo "var book = '$book';";
?>

checkStatus();

function checkStatus()
{
    var requestUrl = encodeURI('conv_status.php?key=' + key);

    // callback
    var callback =
    {
        success: successHandler,
        failure: failureHandler
    };
    
    // Initiate the HTTP GET request.
    YAHOO.util.Connect.asyncRequest('GET', requestUrl, callback);
}

function successHandler(o)
{
    var response = eval("(" + o.responseText + ")");
    
    // display status
    if (response.status == 'r')
    {
        document.getElementById("status").innerHTML = 
            '<h3 class="left">Книга ' + book + ' успешно сконвертированна.</h3>' +
            '<p>Теперь Вы можете <b><a href="' + response.converted + '">загрузить сконвертированную книгу</a></b> и записать её в Ваш Sony Reader. ' +
            '(Возможные ошибки и предупреждения, возникшие в результате конвертации Вы можете посмотреть ' +
            '<a href="' + response.log + '">здесь</a>.)</p>' +
            '<p><a href="' + response.source + '">Посмотреть исходный файл.</a><br/>' +
            '<a href="index.php">Сконвертировать ещё одну книгу.</a><br/></p>';
    }
    else if (response.status == 'e')
    {
        document.getElementById("status").innerHTML = 
            '<h3 class="left">При конвертации книги ' + book + ' произошла ошибка. ' +
            'Вы можете посмотреть её <a href="' + response.log + '">здесь</a>.</h3>' +
            '<p>Хотите нам сообщить об ошибке? Это можно сделать <a href="http://groups.google.com/group/fb2pdf-users/about?hl=ru">здесь</a>. ' +
            'Не забудьте скопировать <a href="' + response.log +'">информацию об ошибке</a> в текст Вашего сообщения.</p>' +
            '<p><a href="' + response.source + '">Посмотреть исходный файл.</a><br/>' +
            '<a href="index.php">Сконвертировать ещё одну книгу.</a><br/></p>';
    }
    else
    {
        setTimeout('checkStatus()', 20000);
    }
}

function failureHandler(o)
{
    // display error
    document.getElementById("status").innerHTML = 'Ошибка конвертации. ' + o.statusText;
}

</script>

</body>
</html>
