<?php
require_once 'awscfg.php';
require_once 'fbparser.php';
require_once 's3.php';
require_once 'db.php';
require_once 'sqshelper.php';
require_once 'book_info.php';
require_once 'utils.php';
require_once 'dUnzip2.inc.php';

// Async. book conversion process
class ConvertBook
{
    private $email    = null; 
    
    private $fbFile   = null;
    private $zipFile  = null;
    private $fileName = null;
    
    public  $book     = null;
    public  $bookKey  = null;

    // Error codes for Exception
    const ERR_ILLEGAL_ARG   = 1; // illegal agrument
    const ERR_LOAD          = 2; // unable to load file 
    const ERR_FORMAT        = 3; // unrecognized format
    const ERR_CONVERT       = 4; // conversion error
    const ERR_SIZE          = 5; // file is too big
    
    // db book status constants (private)
    const DB_BOOK_NOT_FOUND = 0; // book not found in the DB
    const DB_BOOK_CONVERTED = 1; // book is already converted
    const DB_BOOK_RECONVERT = 2; // book is converted but with previous conveter's version
    
    // test mode (no amazon, no db)
    const TEST_MODE = false; // set false on prod.
    
    // Process book from file uploaded via POST
    public function convertFromFile($filePath, $fileName, $format, $email = null)
    {
        $this->email = $email;
        
        if (!trim($fileName) || !trim($filePath))
            throw new Exception("File is not specified.", self::ERR_ILLEGAL_ARG);
            
        if (!is_uploaded_file($filePath))
            throw new Exception("Possible file upload attack: $filePath", self::ERR_LOAD);
            
        // Move uploaded file
        $tempFile = $this->tempFileName();
        if (!move_uploaded_file($filePath, $tempFile))
            throw new Exception("Unable to move uploaded file from $filePath to $tempFile", self::ERR_LOAD);

        // Process book
        $exc = null;
        try
        {
  	    $this->convert($tempFile, $fileName, $format);
        }
        catch (Exception $e)
        {
            $exc = $e;
        }
        
        // Remove temporary files
        $this->cleanupTempFiles();
            
        // exception handling
        if ($exc)
            throw $exc;
    }
    
    // Process book from url
    public function convertFromUrl($url, $format, $email = null)
    {
        $this->email = $email;
        
        if (!trim($url))
            throw new Exception("URL is not specified.", self::ERR_ILLEGAL_ARG);
            
        // Copy file 
        $tempFile = $this->tempFileName();
        if (!copy($url, $tempFile))
            throw new Exception("Unable to copy file from $url to $tempFile", self::ERR_LOAD);

        // Process book
        $exc = null;
        try
        {
	  $this->convert($tempFile, $url, $format);
        }
        catch (Exception $e)
        {
            $exc = $e;
        }
        
        // Remove temporary files
        $this->cleanupTempFiles();
            
        // exception handling
        if ($exc)
            throw $exc;
    }
    
    // This method should be called from callback when conversion is done
    public function converted($email, $password, $key, $status, $ver, $format)
    {
        global $secret;
        
        if (!$key)
            throw new Exception("Invalid key.", self::ERR_ILLEGAL_ARG);
        if ($status != "r" and $status != "e")
            throw new Exception("Invalid status.", self::ERR_ILLEGAL_ARG);

        // check password
        if ($password != md5($secret . $key))
            throw new Exception("Invalid password.", self::ERR_ILLEGAL_ARG);

        if (!self::TEST_MODE)
        {
            // update status in the DB
            $db = getDBObject();
            if (!$db->updateBookStatus($key, $status, $ver, $format))
                error_log("FB2PDF ERROR. Unable to update book status. Key=$key"); 

            // send email to user
            $this->notifyUserByEmail($email, $key, $status);
        }
    }
    
    // Convert file
    private function convert($filePath, $fileName, $format)
    {
        $this->zipFile  = null;
        $this->fbFile   = null;
        
        // Extract fb2 from zip
        $zipArr = $this->unzip($filePath);
        if ($zipArr === false) //  not a zip file
        {
            $this->zipFile = null;
            $this->fbFile  = $filePath;
        }
        else // zip file
        {
            $this->zipFile = $filePath;
            $this->fbFile  = $zipArr["filePath"];
            $fileName      = $zipArr["fileName"];
        }
        
        // Parse fb2
        $parser = new FBParser();
        $this->book = $parser->parse($this->fbFile);
        if ($this->book === false)
            throw new Exception("$fileName is not a fb2 or zip file", self::ERR_FORMAT);
        
        // genarate unique book key
        $this->bookKey = md5(uniqid(""));
        
        // get md5 of the file content (
        // NOTE! Here is a BUG. We should calculate md5 based on full book content (md5file), but we can do it only after reconverting all books.
        $md5 = md5($fileName);
        
        // get the filename without extension
        $this->fileName = $this->getBaseFileName($fileName);
        if (!$this->fileName)
            $this->fileName = $this->bookKey . ".zip";

        // process book
        if (!self::TEST_MODE)
        {
            if (!$this->checkBook($md5))
            {
  	        $this->insertBook($md5);
            }
            
	    $status = $this->checkFormat($format);
            if ($status == self::DB_BOOK_CONVERTED) // book is up-to-date
            {
                 $this->notifyUserByEmail($this->email, $this->bookKey, "r");
                 return;
            }
            if ($status == self::DB_BOOK_NOT_FOUND)
            {
                $this->insertFormat($format);
            }
            else if ($status == self::DB_BOOK_RECONVERT)
            {
                // Prepare book for reconverting 
                $this->updateFormat($format);
            }
            
            // Send request to convert book
            $this->requestConvert($format);
        }
    }
    
    // Extract fb2 from zip file.
    // Returns associative array ("fileName" - name of the file, "filePath" - local path to unzipped fb2 file) or false if the file is not zip archive.
    private function unzip($zipfile)
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
                    $tempFile = $this->tempFileName();
                    $zip->unzip($fileName, $tempFile);
                    
                    $ret = array("fileName"=>$fileName, "filePath"=>$tempFile);
                    break;
                }
            }
        }
        $zip->close();
        return $ret;
    }
    
    private function checkBook($md5)
    {
        $db = getDBObject();
        $bookInfo = $db->getBookByMd5($md5);
        if ($bookInfo)
        {
            $this->bookKey = $bookInfo["storage_key"];
            return TRUE;
        }
        
        return FALSE;
    }
    
    // Insert a new book to be converted
    private function insertBook($md5)
    {
        global $awsS3Bucket;
        
        // save fb2 file
        $s3 = getS3Object();
        
        $httpHeaders = array("Content-Disposition"=>"attachement; filename=\"$this->fileName.fb2\"");
        if (!$s3->writeFile($awsS3Bucket, $this->bookKey . ".fb2", $this->fbFile, "application/fb2+xml", "public-read", "", $httpHeaders))
            throw new Exception("Unable to store file $this->bookKey.fb2 in the Amazon S3 storage.", self::ERR_CONVERT);
        
        // save to DB
        $db = getDBObject();
        
        if (!$db->insertBook($this->bookKey, $this->book->author, $this->book->title, $this->book->isbn, $md5))
        {
            error_log("FB2PDF ERROR. Unable to insert book with key $this->bookKey.zip into DB."); 
            // do not stop if DB is failed!
        }
    }
    
    // Update an existing book to be reconverted 
    private function updateFormat($format)
    {
        global $awsS3Bucket;
        
        // update book status in the DB
        $db = getDBObject();
        
        if (!$db->updateBookStatus($this->bookKey, "p", 0, $format))
        {
            error_log("FB2PDF ERROR. Callback: Unable to update book status. Key=$$this->bookKey"); 
            // do not stop if DB is failed!
        }

        $s3 = getS3Object();
        $zipFile = getStorageName($this->bookkey, $format, ".zip");
        if (!$s3->deleteObject($awsS3Bucket, $zipFile))
        {
            error_log("FB2PDF ERROR. Unable to delete converted file $zipFile from the Amazon S3 storage."); 
            // do not stop if failed!
        }

        $txtFile = getStorageName($this->bookKey, $format, ".txt");
        if (!$s3->deleteObject($awsS3Bucket, $txtFile))
        {
            error_log("FB2PDF ERROR. Unable to delete log file $txtFile from the Amazon S3 storage."); 
            // do not stop if failed!
        }
    }
    
    // Returns status of specified format 
    private function checkFormat($format)
    {
        global $convVersion;
        
        $db = getDBObject();
          
        // check if this book already exists
        $status = self::DB_BOOK_NOT_FOUND;
        
        $bookInfo = $db->getBookStatus($this->bookKey, $format);
        if ($bookInfo)
        {
            // check error status and converter version
            $bookStatus = $bookInfo["status"];
            $bookVer    = $bookInfo["conv_ver"];
            if (($bookStatus == 'r' and $bookVer >= $convVersion) or $bookStatus == 'p') 
            {
                $status = self::DB_BOOK_CONVERTED;
            }
            else 
            {
                error_log("FB2PDF INFO. Books $this->bookKey needs to be converted again. Status=$bookStatus, Version=$bookVer"); 
                $status = self::DB_BOOK_RECONVERT;
            }
        }
        return $status;
    }

    // Returns TRUE if specified format was successfully inserted 
    private function insertFormat($format)
    {
        $db = getDBObject();
        if (!$db->insertBookFormat($this->bookKey, $format))
        {
            error_log("FB2PDF ERROR. Unable to insert book format $format for book $this->bookKey into DB."); 
            return TRUE;
        }

        return FALSE;
    }
    
    // Send request to convert book
    private function requestConvert($format)
    {
        global $awsS3Bucket, $secret;
        
        // send SQS message
        $callbackUrl = getFullUrl("conv_callback.php");

        $db =  getDBObject();

        $formatParams = $db->getFormatParameters($format);

        if(!sqsPutMessage($this->bookKey, "http://s3.amazonaws.com/$awsS3Bucket/$this->bookKey.fb2", $this->fileName, $callbackUrl, md5($secret . $this->bookKey), $this->email, $format, $formatParams))
            throw new Exception("Unable to send Amazon SQS message for key $this->bookKey.", self::ERR_CONVERT);
    }

    // Send notification email to user
    private function notifyUserByEmail($email, $key, $status)
    {
        if ($email)
        {
            $statusUrl = getFullUrl("status.php?key=$key");
    
            $subject = "Your book";
            $message = "<html><body>";
    
            if ($status == "r")
                $message .= "Ваша книга была успешно сконвертированна.";
            else if ($status == "e")
                $message .= "При конвертации Вашей книги произошла ошибка.";
    
            $message .= "<br><a href=\"$statusUrl\">Посмотреть результат конвертации</a>";
            $message .= "</body></html>";

            $headers  = 'MIME-Version: 1.0' . "\r\n";
            $headers .= 'Content-type: text/html; charset=utf-8' . "\r\n"; 
            $headers .= 'From: FB2PDF <noreply@codeminders.com>' . "\r\n";
            
            mail($this->email, $subject, $message, $headers);
        }
    }
    
    // Cleanup temporarly stored files
    private function cleanupTempFiles()
    {
        if ($this->zipFile and !unlink($this->zipFile))
            error_log("FB2PDF WARN. Unable to remove temporary file $this->zipFile"); 
        if ($this->fbFile and !unlink($this->fbFile))
            error_log("FB2PDF WARN. Unable to remove temporary file $this->fbFile"); 
    }
    
    // Generate temporary file name
    private function tempFileName()
    {
        return tempnam(md5(uniqid(rand(), TRUE)), '');
    }
    
    // Returns filename without path and extension
    private function getBaseFileName($fileName)
    {
        $pathParts = pathinfo($fileName);
        $name = removeExt($pathParts["basename"]);
        return $name;
    }
}

// Check book status
class BookStatus
{
    public $fbFile  = null;  // url to original FB2 file
    public $pdfFile = null;  // url to converted ZIP/PDF file
    public $logFile = null;  // url to converted ZIP/PDF file
    
    // book status constants
    const STATUS_PROGRESS = 'p';
    const STATUS_SUCCESS  = 'r';
    const STATUS_ERROR    = 'e';

    // Check status. Returns STATUS_* constants
    // format 0 mean check original only
    public function checkStatus($key, $format = 0)
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

        if ($format != 0)
        {
            $pdfName = getStorageName($key, $format, ".pdf"); 
            $zipName = getStorageName($key, $format, ".zip");
            $logName = getStorageName($key, $format, ".txt");

            // PDFs can be found only for books that where added through early versions of fb2pdf,
            // when there was no support for formats. There is no need to quiry them
            // if format is set to semething other then 1.
            $pdfExists = ($format == 1) && $s3->objectExists($awsS3Bucket, $pdfName);
            $zipExists = $s3->objectExists($awsS3Bucket, $zipName);
            $logExists = $s3->objectExists($awsS3Bucket, $logName);
        
            // check status and generate links
            $status = self::STATUS_PROGRESS;
        
            if (($pdfExists or $zipExists) and $logExists)
            {
                $status = self::STATUS_SUCCESS;
                $this->pdfFile = ($pdfExists) ? "getfile.php?key=$pdfName" : "getfile.php?key=$zipName";
                $this->logFile = "getfile.php?key=$logName";
            }
            else if ($logExists)
            {
                $status = self::STATUS_ERROR;
                $this->logFile = "getfile.php?key=$logName";
            }
        }
        else
        {
            $status = self::STATUS_SUCCESS;
        }
        return $status;
    }
}
?>
