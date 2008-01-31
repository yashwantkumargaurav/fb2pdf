<?php
require_once 'book_info.php';

class FBParser
{
    var $rootElement;
    var $stack = array();

    var $ROOT = "fictionbook";
    var $PATH_FN   = array("fictionbook", "description", "title-info", "author", "first-name");
    var $PATH_LN   = array("fictionbook", "description", "title-info", "author", "last-name");
    var $PATH_BT   = array("fictionbook", "description", "title-info", "book-title");
    var $PATH_ISBN = array("fictionbook", "description", "publish-info", "isbn");
    
    var $title;
    var $firstName;
    var $lastName;
    var $isbn;
    
    
    // Parse fb2 file. 
    // Return BookInfo object if this is fb2 format or false.
    function parse($fbfile)
    {
        // Read the data from file
        $data = NULL;
        $fp = fopen($fbfile,"r");
        if ($fp)
        {
            $data = fread($fp,1024);
            fclose($fp);
        }
        if (!$data)
            return false;
    
        // Initialize the XML parser
        $parser = xml_parser_create();
        xml_set_object($parser, $this);

        xml_set_element_handler($parser, "tagStart", "tagEnd");
        xml_set_character_data_handler($parser, "tagContent");

        if (!xml_parse($parser, $data, false))
        {
            $errMsg = xml_error_string(xml_get_error_code($parser));
            error_log("FB2PDF ERROR. Unable parse XML: $errMsg"); 
            
            xml_parser_free($parser);
            return false;
        }
    
        xml_parser_free($parser);
        
        if ($this->rootElement != $this->ROOT)
            return false;
            
        return $this->getBookInfo();
    }

    function tagStart($parser, $tagName, $attributes)
    {
        array_push($this->stack, strtolower($tagName));
        if (count($this->stack) == 1)
            $this->rootElement = $this->stack[0];
    }

    function tagEnd($parser, $tagName)
    {
        array_pop($this->stack);
    }

    function tagContent($parser, $content)
    {
        if ($this->stack == $this->PATH_FN)
            $this->firstName = $content;
        else if ($this->stack == $this->PATH_LN)
            $this->lastName = $content;
        else if ($this->stack == $this->PATH_BT)
            $this->title = $content;
        else if ($this->stack == $this->PATH_ISBN)
            $this->isbn = $content;
    }
    
    function getBookInfo()
    {
        if ($this->lastName and $this->firstName)
            $author = $this->lastName . ", " . $this->firstName;
        else
            $author = ($this->lastName) ?  $this->lastName : $this->firstName;
        
        return new BookInfo($this->title, $author, $this->isbn); 
    }
    
}

?>