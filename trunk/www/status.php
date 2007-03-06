<?php
require_once 'awscfg.php';
require_once 's3.php';

define('STATUS_PROGRESS',  0);
define('STATUS_DONE',      1);
define('STATUS_ERROR',     2);

global $awsS3Bucket;

$id = $_GET['id'];
$status = getStatus($id);

$originalFile  = "http://s3.amazonaws.com/$awsS3Bucket/$id.fb2";
$convertedFile = "http://s3.amazonaws.com/$awsS3Bucket/$id.pdf";
$logFile       = "http://s3.amazonaws.com/$awsS3Bucket/$id.txt";

function getStatus($id)
{
    global $awsApiKey, $awsApiSecretKey, $awsS3Bucket;
    
    $s3 = new S3($awsApiKey, $awsApiSecretKey);
    $pdffile = $s3->objectExists($awsS3Bucket, $id . ".pdf");
    $logfile = $s3->objectExists($awsS3Bucket, $id . ".txt");
    
    if ($pdffile)
        return STATUS_DONE;
    else
        return ($logfile) ? STATUS_ERROR : STATUS_PROGRESS;
}
?>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>

<?php
if ($status == STATUS_PROGRESS)
    echo "<meta http-equiv=\"refresh\" content=\"30\">";
?>

</head>
<body>

<?php

if ($status == STATUS_DONE)
{
    echo "<h4 align=\"center\">Ваш файл был успешно сконвертирован. Теперь Вы можете <a href=\"$convertedFile\">загрузить</a> сконветрированный файл и записать его в Ваш Sony Reader.";
    echo "<br>(Возможные ошибки и предупреждения, возникшие в результате конвертации Вы можете посмотреть <a href=\"$logFile\">здесь</a>.)</h4>";
    echo "<br><br><a href=\"$originalFile\">Посмотреть исходный файл.</a>";
}
else if ($status == STATUS_ERROR)
{
    echo "<h4 align=\"center\">При конвертации произошла ошибка. Вы можете посмотреть её <a href=\"$logFile\">здесь</a>.</h4>";
    echo "<br><br><a href=\"$originalFile\">Посмотреть исходный файл.</a>";
}
else
{
    echo "<h4 align=\"center\">Конвертация Вашего файла может занять около пяти минут. Пожалуйста, подождите...</h4>"; 
    echo "<div style=\"text-align:center\"><img src=\"images/progress_conv.gif\"/></div>";
    echo "<p>Эта страница обновится автоматически, когда процесс конвертации будет закончен.";
    echo "Вы можете также сохранить URL этой страницы и вернуться к ней в любое удобное для Вас время, чтобы забрать готовый сконвертированный файл.";
}

?>

<br><br><a href="index.php">Сконвертировать ещё один файл.</a>
<br><br>Обнаружили ошибку? У Вас есть предложения по улучшению сервиса? Хотите оставить комментарий?
<br>Это можно сделать <a href="http://groups.google.com/group/fb2pdf-users/about?hl=ru">здесь</a>.

<hr WIDTH="100%">
<a href="http://www.crocodile.org/"><img src="http://www.crocodile.org/noir.png"></a> 

</body>
</html>
