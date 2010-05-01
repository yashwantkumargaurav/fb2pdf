<?php
require_once 'awscfg.php';
require_once 's3.php';
require_once 'db.php';
require_once 'utils.php';


// Check book status
class BookStatus
{
    public $fbFile  = null;  // url to original FB2 file
    public $convFile = null;  // url to converted file
    public $logFile = null;  // url to log file
    
    // book status constants
    const STATUS_PROGRESS = 'p';
    const STATUS_SUCCESS  = 'r';
    const STATUS_ERROR    = 'e';

    // Check status of the original book
    public function checkOriginal($key)
    {
        global $awsS3Bucket;
    
        // check existance
        $s3 = getS3Object();

        // This info is never used. It is 'just in case' check,
        // which requires an extra query. Is it really necessary?
        $fbExists  = $s3->objectExists($awsS3Bucket, $key . ".fb2");
        if (!$fbExists)
            throw new Exception("$key.fb2 does not exist.");

        $this->fbFile = "getfile.php?key=$key.fb2";
    }
    
    // Check converted book status. Returns STATUS_* constants
    public function checkConverted($key, $format, $fileType = "", $compress = "")
    {
        global $awsS3Bucket;

        if ($fileType == "" or $compress == "")
        {
            // update status in the DB
            $db = getDBObject();
            $formatInfo = $db->getFormat($format);
            $fileType = $formatInfo["filetype"];
            $compress = $formatInfo["compress"];
        }
        
        // check existance
        $s3 = getS3Object();

        $pdfName = getStorageName($key, $format, ".pdf");
        if ($compress != "none")
        {
            $convName = getStorageName($key, $format, ".$compress");
        }
        else
        {
            $convName = getStorageName($key, $format, ".$fileType");
        }
        $logName = getStorageName($key, $format, ".txt");

        // PDFs can be found only for books that where added through early versions of fb2pdf,
        // when there was no support for formats. There is no need to query them
        // if format is set to semething other then 1.
        $pdfExists = ($format == 1) && $s3->objectExists($awsS3Bucket, $pdfName);
        $convExists = $s3->objectExists($awsS3Bucket, $convName);
        $logExists = $s3->objectExists($awsS3Bucket, $logName);
        
        // check status and generate links
        $status = self::STATUS_PROGRESS;
        
        if (($pdfExists or $convExists) and $logExists)
        {
            $status = self::STATUS_SUCCESS;
            $this->convFile = ($pdfExists) ? "getfile.php?key=$pdfName" : "getfile.php?key=$convName";
            $this->logFile = "getfile.php?key=$logName";
        }
        else if ($logExists)
        {
            $status = self::STATUS_ERROR;
            $this->logFile = "getfile.php?key=$logName";
        }
        return $status;
    }
}
?>
