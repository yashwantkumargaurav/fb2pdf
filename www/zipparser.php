<?php
require_once 'dUnzip2.inc.php';
require_once 'fbparser.php';

// Check zip format
// Returns fb2 filename or false
function check_zip_format($zipfile)
{
    $ret = false;
    $zip = new dUnzip2($zipfile);
    $zip->debug = false;
    
    $list = $zip->getList();
    if ($list)
    {
        foreach($list as $fileName=>$zippedFile)
        {
      		if (substr($fileName, -1) != "/") // it's not a DIR
            {
                // unzip to a temporary file
                $tempFile = tempnam (md5(uniqid(rand(), TRUE)), '');
                $zip->unzip($fileName, $tempFile);
                
                // check fb format
                if (check_fb_format($tempFile))
                {
                    $ret = $tempFile;
                    break;
                }
                else
                {
                    // remove temporary file
                    unlink($tempFile);
                }
            }
        }
    }
    else
    {
        // not a zip file
        $ret = false;
    }
    $zip->close();
    return $ret;    
}
?>