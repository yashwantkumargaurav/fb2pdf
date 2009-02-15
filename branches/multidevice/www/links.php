<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<?php include 'analytics.inc.php'; ?>
</head>

<body>
<center>
<div id="container" class="WidthPage">
    <?php 
    include 'header.inc.php'; 
    $active_menu = 'links';
    include 'menu.inc.php'; 
    ?>
    
    <div id="tab_box">
        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
        <div class="tab_box_content">
            <img src="images/green_px.gif" class="line"/>
            
            <div class="author" style="font-size:100%;">
                <br/><b>Электронные библиотеки с книгами в формате FB2</b><br/><br/>
            </div>
            
            <div style="width: 640px; text-align: left;">
                <p>
                    <a href="http://lib.aldebaran.ru/">Библиотека Альдебаран</a><br/>
                    <a href="http://www.fictionbook.ru/">Библиотека FictionBook</a><br/>
                    <a href="http://lib.rus.ec/">Либрусек - библиотека в Эквадоре</a><br/>
                    <a href="http://fanlib.ru/">Библиотека FanLib</a><br/>
                    <a href="http://fenzin.org/">Фензин - сайт о фантастике и фэнтези</a><br/>
                    <a href="http://www.litportal.ru/">Литературный портал</a><br/>
                    <a href="http://www.bookz.ru/">Электронная библиотека bookZ.ru</a><br/>
                </p>
            </div>

            <img src="images/green_px.gif" class="line"/>
            <div class="author" style="font-size:100%;">
                <br/><b>Полезные программы</b><br/><br/>
            </div>
            <div style="width: 640px; text-align: left;">
                <p>Если Вы используете FireFox, установите себе специальное расширение, которое позволит Вам конвертировать книги прямо с вэб сайта любой электронной библиотеки, в которой есть книги в FB2 формате. Для установки надо:<br/>
                1. Установить Greasemonkey FireFox Extension. Это можно сделать <a href="https://addons.mozilla.org/en-US/firefox/addon/748">здесь</a><br/>
                2. Нажать на <a href="http://fb2pdf.com/fb2pdflink.user.js">эту ссылку</a>.<br/><br/>
                Теперь, при заходе на сайт электронной библиотеки, возле ссылки на книгу в формате FB2 появится ссылка на конвертацию этой книги для чтения в SonyReader: <u>[SonyReader PDF]</u>.<br>
                Нажимайте на эту ссылку и выбранная Вами книга будет сконвертированна!
                </p>
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
</body>
</html>
