<?php
require_once 'awscfg.php';
require_once 'utils.php';

global $secret;

//$v = var_export($_POST, true);
//error_log("FB2PDF INFO. Callback: POST="); 
//error_log($v); 

$password = trim($_POST['pass']);
$email    = trim($_POST['email']);
$key      = trim($_POST['key']);
$status   = trim($_POST['status']);

// check parameters
if (!$key)
{
    error_log("FB2PDF ERROR. Callback: Missing or wrong parameter key"); 
    send_response("400 Bad Request", "Missing or wrong parameter key");
    die;
}

if ($status != "r" and $status != "e")
{
    error_log("FB2PDF ERROR. Callback: Missing or wrong parameter status"); 
    send_response("400 Bad Request", "Missing or wrong parameter status");
    die;
}

// check password
if ($password != md5($secret . $key))
{
    error_log("FB2PDF ERROR. Callback: Incorrect password"); 
    send_response("400 Bad Request", "Incorrect password");
    die;
}

// update status in the DB
//TODO

// send email to user
if ($email)
{
    //TODO: Strip out ".pdf" from the key
    $statusUrl = get_page_url("status.php?id=$key");
    
    $subject = "Your book is ready";
    
    $message = "<html><body>";
    $message .= "<h4 align=\"center\"><a href=\"$statusUrl\">Посмотреть результат конвертации</a>";
    $message .= "</body></html>";

    $headers  = "MIME-Version: 1.0" . "\r\n";
    $headers .= "Content-type: text/html; charset=utf-8" . "\r\n";    
    
    //mail($email, $subject, $message, $headers);
}

error_log("FB2PDF INFO. Callback: password=$password, key=$key, status=$status, email=$email"); 
send_response("200 OK", "");

function send_response($httpCode, $message)
{
    header("HTTP/1.0 $httpCode");
    header('Content-type: text/html');    
    if ($message)
        echo "<html><body>$message</body></html>";
}

?>