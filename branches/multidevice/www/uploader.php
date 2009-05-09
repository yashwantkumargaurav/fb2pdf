<?php
require_once 'process.php';
require_once 'utils.php';

$url = (isset($_GET["url"])) ? $_GET["url"] : null;
$email = $_POST['email'];
$format = $_POST['format'];

$conv = new ConvertBook();
$file = null;
try
{
    if ($url || $_POST['uploadtype'] == 'url')
    {
        $file = ($url) ? $url : $_POST['url'];
            
        $conv->convertFromUrl($file, $email, $format);
    }
    else if ($_POST['uploadtype'] == 'file')
    {
        $err_upload = $_FILES['fileupload']['error'];
        if ($err_upload == UPLOAD_ERR_OK)
        {
            // check uploaded file
            $path = $_FILES['fileupload']['tmp_name'];
            $file = $_FILES['fileupload']['name'];
            
            $conv->convertFromFile($path, $file, $email, $format);
        }
        else
        {
            // deal with errors
            if ($err_upload == UPLOAD_ERR_INI_SIZE || $err_upload == UPLOAD_ERR_FORM_SIZE)
                throw new Exception("The uploaded file exceeds the maximum allowed size.", ConvertBook::ERR_SIZE);
            else
                throw new Exception("Unable to upload file. PHP error - " . $err_upload, ConvertBook::ERR_LOAD);
        }
    }
    
    $key = $conv->bookKey;
    httpRedirect("status.php?key=$key");
}
catch(Exception $e)
{
    error_log("FB2PDF ERROR. Uploader: " . $e->getMessage()); 
    
    $errCode = null;
    $errMessage = null;
    if ($e->getCode() == ConvertBook::ERR_ILLEGAL_ARG)
    {
        $errCode = "400 Bad Request";
        $errMessage = "Пожалуйста, укажите FB2 файл, который Вы бы хотели сконвертировать.";
    }
    else if ($e->getCode() == ConvertBook::ERR_LOAD)
    {
        $errCode = "400 Bad Request";
        $errMessage = "Невозможно загрузить файл <b>$file</b>. Пожалуйста, убедитесь, что Вы правильно указали имя файла и попробуйте ешё раз.";
    }
    else if ($e->getCode() == ConvertBook::ERR_FORMAT)
    {
        $errCode = "404 Not Found";
        $errMessage = "<b>$file</b> не существует или не является файлом в формате ZIP или FB2. Пожалуйста, выберите ZIP или FB2 файл и попробуйте ещё раз.";
    }
    else if ($e->getCode() == ConvertBook::ERR_CONVERT)
    {
        $errCode = "500 Internal Server Error";
        $errMessage = "Невозможно сохранить файл <b>$file</b> для дальнейшей конвертации. Пожалуйста, попробуйте ешё раз.";
    }
    else if ($e->getCode() == ConvertBook::ERR_SIZE)
    {
        $errCode = "400 Bad Request";
        $errMessage = "Размер файла <b>$file</b> превышает максимально допустимый.";
    }
    
    httpResponseCode($errCode, $errMessage);
}
?>
