<?php
require_once 'awscfg.php';
require_once 's3.php';

define('STATUS_PROGRESS',  0);
define('STATUS_DONE',      1);
define('STATUS_ERROR',     2);

if (!isset ($_GET['id']))
{
    header("HTTP/1.0 400 Bad Request");
    header('Content-type: text/html');    
    echo "<html><body>Missing \"id\" paremeter</body></html>";
    die;
}
$id = $_GET['id'];

global $awsS3Bucket;


// remove "extension" part from the key
$pos = strrpos($id, ".");
if ($pos !== false) 
    $id = substr($id, 0, $pos);

$res = getStatus($id);

$originalFile  = "getfile.php?key=$id.fb2";

$convertedFile = "getfile.php?key=" . $res["convertedFile"];
$logFile       = "getfile.php?key=" . $res["logFile"];
$status        = $res["status"];

function getStatus($id)
{
    global $awsApiKey, $awsApiSecretKey, $awsS3Bucket;
    
    $s3 = new S3($awsApiKey, $awsApiSecretKey);
    $pdffile = $s3->objectExists($awsS3Bucket, $id . ".pdf");
    $zipfile = $s3->objectExists($awsS3Bucket, $id . ".zip");
    $logfile = $s3->objectExists($awsS3Bucket, $id . ".txt");
    
    $res = array();
    if (($pdffile or $zipfile) and $logfile)
    {
        $res["status"] = STATUS_DONE;
        $res["convertedFile"] = ($pdffile) ? "$id.pdf" : "$id.zip";
        $res["logFile"] = "$id.txt";
    }
    else if ($logfile)
    {
        $res["status"] = STATUS_ERROR;
        $res["convertedFile"] = NULL;
        $res["logFile"] = "$id.txt";
    }        
    else
    {
        $res["status"] = STATUS_PROGRESS;
        $res["convertedFile"] = NULL;
        $res["logFile"] = NULL;
    }
    return $res;
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

<?php
if ($status == STATUS_PROGRESS)
    echo "<meta http-equiv=\"refresh\" content=\"30\">";
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
            <img src="images/lg_px.gif" class="line"/>
            <div class="message">
                
                <?php
                if ($status == STATUS_DONE)
                {
                    echo "<h3>Ваш файл был успешно сконвертирован.</h3>
                    <p>Теперь Вы можете <b><a href=\"$convertedFile\">загрузить сконветрированный файл</a></b> и записать его в Ваш Sony Reader.
                    (Возможные ошибки и предупреждения, возникшие в результате конвертации Вы можете посмотреть <a href=<a href=\"$logFile\">здесь</a>.)</p>
                    <p>
                    <a href=\"$originalFile\">Посмотреть исходный файл.</a><br/>
                    <a href=\"index.php\">Сконвертировать ещё один файл.</a><br/>
                    </p>";
                }
                else if ($status == STATUS_ERROR)
                {
                    echo "<h3>При конвертации произошла ошибка.<br/> Вы можете посмотреть её <a href=\"$logFile\">здесь</a>.</h3>
                    <p>Хотите нам сообщить об ошибке? Это можно сделать <a href=\"http://groups.google.com/group/fb2pdf-users/about?hl=ru\">здесь</a><br/>
                    Не забудьте скопировать <a href=\"$logFile\">информацию об ошибке</a> в текст Вашего сообщения.</p>
                    <p>
                    <a href=\"$originalFile\">Посмотреть исходный файл.</a><br/>
                    <a href=\"index.php\">Сконвертировать ещё один файл.</a><br/>
                    </p>";
                }
                else
                {
                    echo "<h3 class=\"center\">Конвертация Вашего файла может занять несколько минут.<br/> Пожалуйста, подождите...</h3>
                    <p class=\"center\"><img src=\"images/progress_conv.gif\"/></p>
                    <p>Эта страница обновится автоматически, когда процесс конвертации будет закончен. 
                    Вы можете также сохранить URL этой страницы и вернуться к ней в любое удобное для Вас время, 
                    чтобы забрать готовый сконвертированный файл.</p>
                    <p><a href=\"index.php\">Сконвертировать ещё один файл.</a><br/></p>";
                }
                ?>
            
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
</body>
</html>
