<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<script type="text/javascript">
function toggleuploadmode(file) {
    if (file) {
        document.getElementById('upfile').style.display='block';
        document.getElementById('upurl').style.display='none';
    } else {
        document.getElementById('upfile').style.display='none';
        document.getElementById('upurl').style.display='block';
    }
 }
</script>
</head>
<body>
<h4 align="center">Этот сервис предназначен для конвертации книг из формата <a href="http://ru.wikipedia.org/wiki/FictionBook">FictionBook2(FB2)</a> в формат <a href="http://en.wikipedia.org/wiki/Sony_Reader">Sony Reader</a>.</h4>
<p>Пожалуйста загрузите FB2 файл или укажите URL этого файла:
<p>

<form enctype="multipart/form-data" action="uploader.php" method="POST">

 <input type="radio" name="uploadtype" value="file" onclick="toggleuploadmode(true);" checked /> file
 <input type="radio" name="uploadtype" value="url" onclick="toggleuploadmode(false);" /> url

 <div id="upfile">
 <input type="file" name="fileupload" size="30" id="fileupload"/>
 </div>
 
 <div id="upurl" style="display: none">
 <input type="text" id="fileupload" value="type url here" name="url" size="30"/>
 </div>
 
<input type="submit" value="Upload File" />
</form>

<p>Обнаружили ошибку? У Вас есть предложения по улучшению сервиса? Хотите оставить комментарий?
<br>Это можно сделать <a href="http://groups.google.com/group/fb2pdf-users/about?hl=ru">здесь</a>

</body>
 