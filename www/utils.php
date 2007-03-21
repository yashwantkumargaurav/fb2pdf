<?php
function getFullUrl($page)
{
    $host = $_SERVER["HTTP_HOST"];
    $uri  = rtrim(dirname($_SERVER["PHP_SELF"]), "/\\");

    return "http://$host$uri/$page";
}

function notifyUserByEmail($email, $key)
{
    $statusUrl = getFullUrl("status.php?id=$key");
    
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
    
    mail($email, $subject, $message, $headers);
}
?>