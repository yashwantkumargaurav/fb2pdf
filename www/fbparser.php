<?php
require_once 'book_info.php';

class FBParser
{
    var $rootElement;
    var $stack = array();

    var $ROOT = "fictionbook";
    
	var $hashmap = array(
						'fictionbook, description, title-info, author, first-name' =>  '$this->book_info->add_first_name($content)',
						'fictionbook, description, title-info, author, middle-name' => '$this->book_info->add_middle_name($content)',
						'fictionbook, description, title-info, author, last-name' =>   '$this->book_info->add_last_name($content)',
						'fictionbook, description, title-info, author, nickname' =>    '$this->book_info->add_nickname($content)',
						'fictionbook, description, title-info, author, home-page' =>   '$this->book_info->add_homepage($content)',
						'fictionbook, description, title-info, author, email' =>       '$this->book_info->add_email($content)',
						'fictionbook, description, title-info, book-title' => '$this->book_info->set_title($content)',
						'fictionbook, description, title-info, lang' =>       '$this->book_info->set_lang($content)',
						'fictionbook, description, title-info, genre' =>      '$this->book_info->add_genre($content)',
						
						'fictionbook, description, publish-info, book-name' => '$this->book_info->set_book_name($content)',
						'fictionbook, description, publish-info, publisher' => '$this->book_info->set_publisher($content)',
						'fictionbook, description, publish-info, city' =>      '$this->book_info->set_city($content)',
						'fictionbook, description, publish-info, year' =>      '$this->book_info->set_year($content)',
						'fictionbook, description, publish-info, isbn' =>      '$this->book_info->set_isbn($content)'
						);
	
	var $book_info;
    
    var $parser;
    
	function __construct()
    {
        $this->book_info = new BookInfo();
    }

	
    // Parse fb2 file. 
    // Return BookInfo object if this is fb2 format or false.
    function parse($fbfile)
    {
        // Read the data from file
        $data = NULL;
        $fp = fopen($fbfile,"r");
        if ($fp)
        {
            $data = fread($fp, filesize($fbfile));
            fclose($fp);
        }
        if (!$data)
            return false;
    
        // Initialize the XML parser
        $this->parser = xml_parser_create();
        xml_set_object($this->parser, $this);

        xml_set_element_handler($this->parser, "tagStart", "tagEnd");
        xml_set_character_data_handler($this->parser, "tagContent");

        if (!xml_parse($this->parser, $data, false))
        {
            $errMsg = xml_error_string(xml_get_error_code($this->parser));
            error_log("FB2PDF ERROR. Unable parse XML: $errMsg"); 
            
            xml_parser_free($this->parser);
            return false;
        }
    
        xml_parser_free($this->parser);
        
        if ($this->rootElement != $this->ROOT)
            return false;
            
        return $this->getBookInfo();
    }

    function tagStart($parser, $tagName, $attributes)
    {
        array_push($this->stack, strtolower($tagName));
        if (count($this->stack) == 1)
            $this->rootElement = $this->stack[0];
		
		//Get attribute of date	
		if (implode(", ", $this->stack) == 'fictionbook, description, document-info, date')
			$this->book_info->set_date($attributes["VALUE"]);
			
		//Add tag to description
		if (strpos(implode(", ", $this->stack), 'fictionbook, description, title-info, annotation, ') !== false)
			$this->book_info->add_description("<". strtolower($tagName) .">");
    }

    function tagEnd($parser, $tagName)
    {
		//Count++ if end of author tag
		if (implode(", ", $this->stack) == 'fictionbook, description, title-info, author')
			$this->book_info->add_count();
		
		//Add tag to description
		if (strpos(implode(", ", $this->stack), 'fictionbook, description, title-info, annotation, ') !== false)
			$this->book_info->add_description("</". strtolower($tagName) .">");
			
        array_pop($this->stack);
    }

    function tagContent($parser, $content)
    {
		if (array_key_exists(implode(", ", $this->stack), $this->hashmap))
			eval($this->hashmap[implode(", ", $this->stack)] . ";");
		
		//Add everything with the base of 'fictionbook, description, title-info, annotation'(description)
		if (strpos(implode(", ", $this->stack), 'fictionbook, description, title-info, annotation') !== false)
			$this->book_info->add_description($content);
    }
	
    function getBookInfo()
    {        
        return $this->book_info; 
    }   
}
?>
