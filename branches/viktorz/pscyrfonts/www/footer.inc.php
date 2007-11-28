<?php
	/*
	$author  =  $_GET["author"];
	$base    =  "atom.php";
	$link    =  (isset($author)) ? "$base?author=$author" : $base;
	*/
	$link = "atom.php";
?>
<p class="end_line">Обнаружили ошибку? У Вас есть предложения по улучшению сервиса? Хотите оставить комментарий?
<br/>Это можно сделать <a href="http://groups.google.com/group/fb2pdf-users/about?hl=ru">здесь</a>
<div></div>
<?php
echo "
<a href=\"$link\">
";
?>
<img src="images/atom.gif"/></a>&nbsp;&nbsp;<a href="http://www.crocodile.org/"><img src="images/noir.png" class="left" width="80" height="15"></a>
<div>
    <script type="text/javascript" src="http://www.crocodile.org/linknet/adblock.php?lang=en,ru&charsset=koi8-r"></script>
</div>