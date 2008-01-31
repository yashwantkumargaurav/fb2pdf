<?php
require_once 'process.php';
require_once 'utils.php';

$url = (isset($_GET["url"])) ? $_GET["url"] : null;
$email = $_POST['email'];

$conv = new ConvertBook();
$file = null;
try
{
    if ($url || $_POST['uploadtype'] == 'url')
    {
        $file = ($url) ? $url : $_POST['url'];
            
        $conv->convertFromUrl($file, $email);
    }
    else if ($_POST['uploadtype'] == 'file')
    {
        // check uploaded file
        $path = $_FILES['fileupload']['tmp_name'];
        $file = $_FILES['fileupload']['name'];
        
        $conv->convertFromFile($path, $file, $email);
    }
    
    $key = $conv->bookKey;
    httpRedirect("status.php?key=$key");
}
catch(Exception $e)
{
    error_log("FB2PDF ERROR. Uploader: " . $e->getMessage()); 
    
    $errMessage = null;
    if ($e->getCode() == ConvertBook::ERR_ILLEGAL_ARG)
        $errMessage = "Пожалуйста, укажите FB2 файл, который Вы бы хотели сконвертировать.";
    else if ($e->getCode() == ConvertBook::ERR_LOAD)
        $errMessage = "Невозможно загрузить файл <b>$file</b>. Пожалуйста, убедитесь, что Вы правильно указали имя файла и попробуйте ешё раз.";
    else if ($e->getCode() == ConvertBook::ERR_FORMAT)
        $errMessage = "<b>$file</b> не существует или не является файлом в формате ZIP или FB2. Пожалуйста, выберите ZIP или FB2 файл и попробуйте ещё раз.";
    else if ($e->getCode() == ConvertBook::ERR_CONVERT)
        $errMessage = "Невозможно сохранить файл <b>$file</b> для дальнейшей конвертации. Пожалуйста, попробуйте ешё раз.";
    
    httpResponseCode("400 Bad Request", $errMessage);
}
?>
