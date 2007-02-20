<html>
<body>

<?php
require_once 'fbparser.php';
require_once 'awscfg.php';
require_once 's3.class.php';

$filePath = NULL;
$fileName = NULL;

if ($_POST['uploadtype'] == 'file')
{
    // check uploaded file
    $filePath = $_FILES['fileupload']['tmp_name'];
    $fileName = $_FILES['fileupload']['name'];
    
    if (trim($fileName) == "")
        error("Please, specify a file you would like to convert.");
        
    if (!is_uploaded_file($filePath)) 
        error("Internal error. Unable to upload the file. Please, try again.");
}
else if ($_POST['uploadtype'] == 'url')
{
    $filePath = $_POST['url'];
    $fileName = $filePath;
}

// Check format
print "<br>Checking the file format...";
if (!check_fb_format($filePath))
    error($fileName . " does not exists or it is not a fb2 file. Please select a fb2 file and try again.");
print " Done";

print "<br>Uploading file...";
if (!s3_put($filePath))    
    error("Unable to store file " . $fileName . " for further processing. Please try again.");
print " Done";

// Put file to amazon s3
function s3_put($filePath)
{
    // create a bucket
    return TRUE;
}
    
// Print error message and stop the script
function error($str) 
{
    print "<div style='color: red;'><pre>$str</pre></div>";
    die;
}
?>
</body>
</html>
