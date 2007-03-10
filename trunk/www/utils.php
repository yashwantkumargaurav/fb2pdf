<?php
function get_page_url($page)
{
    $host = $_SERVER["HTTP_HOST"];
    $uri  = rtrim(dirname($_SERVER["PHP_SELF"]), "/\\");

    return "http://$host$uri/$page";
}
?>