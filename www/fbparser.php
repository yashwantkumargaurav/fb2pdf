<?php

$rootElementFound = FALSE;

// Check fb format
// Returns TRUE or FALSE
function check_fb_format($file)
{
    global $rootElementFound;
    
    // Read the data from file
    $data = NULL;
    $fp=fopen($file,"r");
    if ($fp)
    {
        $data=fread($fp,1024);
        fclose($fp);
    }
    if (!$data)
        return FALSE;
    
    // Initialize the XML parser
    $parser=xml_parser_create();
    xml_set_element_handler($parser,"fb_element_start","fb_element_end");
    
    $error = FALSE;
    if (!xml_parse($parser,$data,FALSE))
        $error = TRUE;
    
    xml_parser_free($parser);
    
    return $rootElementFound and !$error;
}

// Function to use at the start of an element
function fb_element_start($parser,$element_name,$element_attrs)
{
    global $rootElementFound;
    
    if ($element_name == "FICTIONBOOK")
        $rootElementFound = TRUE;
}

// Function to use at the end of an element
function fb_element_end($parser,$element_name)
{
}

?>