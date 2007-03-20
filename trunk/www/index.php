<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>

<script type="text/javascript">
function toggleUploadMode(file) 
{
    if (file) 
    {
        document.getElementById('upfile').style.display='block';
        document.getElementById('upurl').style.display='none';
    } else 
    {
        document.getElementById('upfile').style.display='none';
        document.getElementById('upurl').style.display='block';
    }
 }
 
function doUpload()
{
    // hide form
    document.getElementById('form').style.display = 'none';
    // show progress indicator
    document.getElementById('progress').style.display = '';
    // submit form
    document.getElementById('uploadform').submit();
    // hack for IE: when form is submitted, IE stops to load and animate pictures 
    // so we'll ask IE to show picture again _AFTER_ form submission, with some delay (200ms)
    setTimeout('showProgress()', 200);
}

function showProgress()
{
    // refresh image source to start animation
    var o = document.getElementById('pimage');
    if (o)
        o.src = 'images/progress.gif';
}

function showForm()
{
    // hide progress indicator
    document.getElementById('progress').style.display = 'none';
    // show form
    document.getElementById('form').style.display = '';
}

function selectText(source)
{
    if (source)
    {   
        source.focus();
        source.select();
    }
}


</script>
</head>
<body>

<!-- div to display upload form -->
<div id="form">
    <h4 align="center">Этот сервис (альфа версия) предназначен для конвертации книг из формата <a href="http://ru.wikipedia.org/wiki/FictionBook">FictionBook2(FB2)</a> в формат <a href="http://www.anrdoezrs.net/click-2348710-10383604?url=http%3A%2F%2Fwww.sonystyle.com%2Fis-bin%2FINTERSHOP.enfinity%2FeCS%2FStore%2Fen%2F-%2FUSD%2FSY_DisplayProductInformation-Start%3FProductSKU%3DPRS500U2%26CategoryName%3Dpa_portablereader%26DCMP%3DCJ_SS%26HQS%3DPRS500U2&cjsku=PRS-500" target="_blank">Sony Reader</a><img src="http://www.awltovhc.com/image-2348710-10383604" width="1"  height="1" border="0"/>.</h4>
    <p>Пожалуйста загрузите книгу в FB2 или ZIP формате (ZIP может содержать только одну книгу в FB2 формате) или укажите URL.
    <br>Не знаете, где можно найти книги в формате FB2? Мы рекомендуем электронные библиотеки <a href="http://fictionbook.ru/">FictionBook</a> и <a href="http://aldebaran.ru/">АЛЬДЕБАРАН</a>
    <p>

    <form id="uploadform" enctype="multipart/form-data" action="uploader.php" method="POST">
        <input type="radio" name="uploadtype" value="file" onclick="toggleUploadMode(true);" checked /> file
        <input type="radio" name="uploadtype" value="url" onclick="toggleUploadMode(false);" /> url

        <div id="upfile">
            <input type="file" name="fileupload" size="30" id="fileupload"/>
        </div>
 
        <div id="upurl" style="display: none">
            <input type="text" id="fileupload" value="наберите URL здесь" name="url" size="30" onclick="selectText(this);"/>
        </div>
        <br><input type="button" onclick="doUpload()" value="Конвертировать" />
 
        <p>Для удобства, Вы также можете (но не обязаны) указать адрес Вашей электронной почты, и мы пошлём вам письмо, как только книга будет готова. 
        <br><br><sub>Введённый Вами адрес электронной почты используется <u>только</u> для уведомления о готовности книги. 
        Мы гарантируем конфидициальность, и обязуемся <u>не использовать</u> указанный Вами адрес для рассылки рекламы.</sub>
        <p>
        email (не обязательно):
        <br><input type="text" id="email" value="" name="email" size="30"/>
    </form>
    
    <?php
    require_once 'awscfg.php';
    require_once 'db.php';
    require_once 'utils.php';

    global $awsS3Bucket;
    global $dbServer, $dbName, $dbUser, $dbPassword;
    
    // list of new books
    $MAX_BOOKS = 40;
    $MAX_ROWS  = 20;
    $MAX_COLS  = 2;
    
    $db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
    $list = $db->getBooks($MAX_BOOKS);
    if ($list)
    {
        echo '<h4 align="center">Книги, сконвертированные недавно:</h4>';
        echo '<table border="0">';
        
        $count = count($list);
        for ($row = 0; $row < $MAX_ROWS; $row++) 
        {
            echo '<tr>';
            for ($col = 0; $col < $MAX_COLS; $col++) 
            {
                $i = $col * $MAX_ROWS + $row;
                if ($i < $count)
                {
                    $author = $list[$i]["author"];
                    $title  = $list[$i]["title"];
                    $key    = $list[$i]["storage_key"];
                    if (strrpos($key, ".") === false) // old style key (no extension)
                        $key = $key . ".pdf";

                    if (!$author)
                        $author = "Автор неизвестен";
                    if (!$title)
                        $title = "Название неизвестно";
                    
                    echo "<td><i>$author</i>&nbsp;&nbsp;<a href=\"getfile.php?key=$key\">\"$title\"</a></td>";
                    echo '<td width="30"></td>';
                }
            }
            echo '</tr>';
        }
        echo '</table>';
    }
    ?>
    
    <p>Обнаружили ошибку? У Вас есть предложения по улучшению сервиса? Хотите оставить комментарий?
    <br>Это можно сделать <a href="http://groups.google.com/group/fb2pdf-users/about?hl=ru">здесь</a>
</div>

<!-- div to display progress indicator -->
<div id="progress" style="display:none;text-align:center">
    <h4 align="center">Загрузка файла. Пожалуйста, подождите...</h4> 
    <img id="pimage" src="images/progress.gif"/>
</div>

<hr WIDTH="100%">
<a href="http://www.crocodile.org/"><img src="http://www.crocodile.org/noir.png"></a> 

</body>
 