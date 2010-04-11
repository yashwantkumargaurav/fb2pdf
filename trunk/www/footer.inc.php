<script type="text/javascript">
YAHOO.example.BasicRemote = function() {
    // Use an XHRDataSource
    var oDS = new YAHOO.util.XHRDataSource("search_rpc.php");
    // Set the responseType
    oDS.responseType = YAHOO.util.XHRDataSource.TYPE_TEXT;
    // Define the schema of the delimited results
    oDS.responseSchema = {
        recordDelim: "\n",
        fieldDelim: "\t"
    };
    // Enable caching
    oDS.maxCacheEntries = 5;    
    
    // Instantiate the AutoComplete
    var oAC = new YAHOO.widget.AutoComplete("myInput", "myContainer", oDS);
    oAC.allowBrowserAutocomplete = false;
    oAC.autoHighlight = false;
    
    return {
        oDS: oDS,
        oAC: oAC
    };
}();
</script>
<?php
$base    =  "atom.php";
$link    =  isset($_GET["author"]) ? ("$base?author=".$_GET["author"]) : $base;
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
