<?php
function formatDateIntoAtom($date)
{
	$date = str_replace(" ", "T", $date. "Z");
	return $date;
}
function getFullUrl($page)
{
    $host = $_SERVER["HTTP_HOST"];
    $uri  = rtrim(dirname($_SERVER["PHP_SELF"]), "/\\");

    return "http://$host$uri/$page";
}

function httpResponseCode($httpCode, $message=null)
{
    header("HTTP/1.0 $httpCode");
    header('Content-type: text/html');    
    
    if ($message)
        echo "<html><body>$message</body></html>";
}

function httpRedirect($url)
{
    header("HTTP/1.0 302 Found");
    header("Location: $url");
}

function removeExt($name)
{
    $pos = strrpos($name, ".");
    if ($pos !== false) 
        $name = substr($name, 0, $pos);

    return $name;
}

function getStorageName($storageKey, $format, $extension = "")
{
    $suffix = ($format != 1) ? "-$format" : "";

    return ($storageKey . $suffix . $extension);
}


?>