<?php

// amazon keys
$awsApiKey = "12MJ51PYW8J9E7SX6882";        // Specify key here
$awsApiSecretKey = "sQRjPkWFfo3/xOcSLWIOgaGJrjtCSbkgfBv6+Kbf";  // Specify secret key here

// amazon s3 storage settings
$awsS3Bucket = "fb2pdf";
//$awsS3Bucket = "fb2pdf_debug";

// amazon Simple Queue Service settings
$awsSQSQueue = "fb2pdftasks";
//$awsSQSQueue = "fb2pdfdebug";
$awsSQSTimeout = 600;

// secret phrase
$secret = "Babushka";   // Specify secret phrase here

// db settings
$dbServer = "localhost";    // Specify DB name here
$dbName = "new";         // Specify DB name here
$dbUser = "root";         // Specify DB user here
$dbPassword = "negowan781";   // Specify DB password here
//$dbUser = "";         // Specify DB user here
//$dbPassword = "";   // Specify DB password here

// converter version
$convVersion = 3.14;
?>
