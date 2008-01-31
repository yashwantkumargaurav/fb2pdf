<?php

$key = "8d07720b6196be4904f660614643fbc7.zip";
$url = "http://s3.amazonaws.com/fb2pdf/$key";
$md5 = md5($url);
$md5_file = md5_file($url);
//$md5 = "123";

echo "url = $url<br>md5 = $md5<br>md5_file = $md5_file"; 

?>