<?php
class BookInfo
{
    public $title;
    public $author;
    public $isbn;
    
    function BookInfo($title, $author, $isbn)
    {
        $this->title  = $title;
        $this->author = $author;
        $this->isbn   = $isbn;
    }
}
?>