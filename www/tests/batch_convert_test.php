<?php
require_once 'HTTP/Request.php';

$request = new HTTP_Request("batch_convert.php");

$httpDate = gmdate("D, d M Y H:i:s T");
$request->setMethod("POST");
$request->addHeader("content-type", "text/xml");
$request->addHeader("Date", $httpDate);

$xmldata = 
'<?xml version = "1.0" encoding = "UTF-8" ?>' .
'<fb2pdfbatchjob version="1"> ' .
    '<source url="http://example.com/book1.fb2.zip" type="application/fb2+xml" encoding="application/zip" name="book 1"/>' .
    '<source url="http://example.com/book2.fb2.zip" type="application/fb2+xml" encoding="application/zip" name="book 2"/>' . 
    '<source url="http://example.com/book3.fb2.zip" type="application/fb2+xml" encoding="application/zip" name="book 3"/>' . 
'</fb2pdfbatchjob>';

$request->setBody($xmldata);
$request->sendRequest();

header("content-type: text/html");
print $request->getResponseBody();

?>