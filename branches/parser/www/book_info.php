<?php
class BookInfo
{
    public $title;
	private $count = 0;
    public $author = array();
	public $genre  = array();
	public $lang;
	public $description;
	public $date;
	
	public $book_name;
	public $publisher;
	public $city;
	public $year;
    public $isbn;
	
	
	function set_title($title)
	{
		$this->title = $title;
	}
	
	function add_first_name($name)
	{
		$this->author[$this->count]["first"] = $name;
	}
	
	function add_middle_name($name)
	{
		$this->author[$this->count]["middle"] = $name;
	}
	
	function add_last_name($name)
	{
		$this->author[$this->count]["last"] = $name;
	}
	
	function add_nickname($name)
	{
		$this->author[$this->count]["nickname"] = $name;
	}
	
	function add_homepage($homepage)
	{
		$this->author[$this->count]["homepage"] = $homepage;
	}
	
	function add_email($email)
	{
		$this->author[$this->count]["email"] = $email;
	}
	
	function add_count()
	{
		$this->count++;
	}
	
	function add_genre($genre)
	{
		$this->genre[] = $genre;
	}
	
	function set_lang($lang)
	{
		$this->lang = $lang;
	}
	
	function add_description($description)
	{
		$this->description .= $description;
	}
	
	function set_date($date)
	{
		$this->date = $date;
	}
	
	function set_book_name($name)
	{
		$this->book_name = $name;
	}
	
	function set_publisher($publisher)
	{
		$this->publisher = $publisher;
	}
	
	function set_city($city)
	{
		$this->city = $city;
	}
	
	function set_year($year)
	{
		$this->year = $year;
	}
	
	function set_isbn($isbn)
	{
		$this->isbn = $isbn;
	}
}
?>