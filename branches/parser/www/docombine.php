<?php

  // TODO:
  // 1. process title
  // 2. process fb.zip
  // 3. preserve order of parts!

$title = $_POST["title"];

$urlfiles = array();
$uploadfiles = array();

if(function_exists('sys_get_temp_dir'))
    $tmp=sys_get_temp_dir();
else
    $tmp="/tmp";

function cleanup()
{
    //remove fetched files
    global $urlfiles, $destfile;
    foreach($urlfiles as $i)
        unlink($i);
    unlink($destfile);
}

register_shutdown_function("cleanup");

foreach(array_keys($_POST) as $i)
{
    if(preg_match('/^url[0-9]+/',$i))
    {
        $url = $_POST[$i];
        $tmpfile = tempnam($tmp, 'fb2part');
        if(!copy($url, $tmpfile))
        {
            header("HTTP/1.0 500 Internal Server Error");
            echo("Error fetching URL: $url");
            return;
        }
        $urlfiles[]=$tmpfile;
    }
}

foreach(array_keys($_FILES) as $i)
    $uploadfiles[]=$_FILES[$i]['tmp_name'];

$destfile = tempnam($tmp, 'fb2combined');

$cmd = "fbmerge -o "
. escapeshellarg($destfile)
. " "
. join(" ",array_map('escapeshellarg',$urlfiles))
. " "
. join(" ",array_map('escapeshellarg',$uploadfiles))
. " 2>&1";

error_log("Executing: " . $cmd);

$cmdout=array();
$cmdout[]="Merge failed with following error: ";
exec($cmd, $cmdout, $rc);
$cmdout_s=join("\n", $cmdout);
if($rc!=0)
{
    error_log($cmdout_s);
    header("HTTP/1.0 500 Internal Server Error");
    echo "Merge failed with the following error: ";
    echo "<pre>" . htmlspecialchars($cmdout_s) . "</pre>";    
    return;
}

header("Cache-Control: must-revalidate, post-check=0, pre-check=0");
header("Content-Type: application/fb2+xml");
header('Content-Disposition: attachment; filename=' . basename($destfile) . ".fb2");

readfile($destfile);

?>
