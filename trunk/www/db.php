<?php

class DB
{
	var $server;
	var $name;
   	var $user;
   	var $password;
    
	function DB($server, $name, $user, $password) 
    {
    	$this->server   = $server;
    	$this->name     = $name;
       	$this->user     = $user;
       	$this->password = $password;
	}
    
    // Insert a new book
    function insertBook($storageKey, $author, $title, $isbn, $md5, $status)
    {
        if(!($link = mysql_connect($this->server, $this->user, $this->password))) 
        {
            error_log("FB2PDF ERROR. Error connecting to the database server");
            return false;
        }

        if(!mysql_select_db($this->name))
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Error selecting database");
            return false;
        }

		$set = @mysql_query ('SET NAMES UTF8');
		$set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');
        
        $author = mysql_real_escape_string($author);
        $title  = mysql_real_escape_string($title);
        $isbn   = mysql_real_escape_string($isbn);
        
        $query = "INSERT INTO Books (storage_key, author, title, isbn, md5_hash, status, converted) 
            VALUES(\"$storageKey\", \"$author\", \"$title\", \"$isbn\", 0x$md5, \"$status\",  UTC_TIMESTAMP())";
        if(!($result = mysql_query($query))) 
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Query failed: $query.\n" . mysql_error());
            return false;
        }
        mysql_close($link);
        return true;
    }
    
    // Updade status
    function updateBookStatus($storageKey, $status)
    {
        if(!($link = mysql_connect($this->server, $this->user, $this->password))) 
        {
            error_log("FB2PDF ERROR. Error connecting to the database server");
            return false;
        }

        if(!mysql_select_db($this->name))
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Error selecting database");
            return false;
        }

		$set = @mysql_query ('SET NAMES UTF8');
		$set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');
        
        $query = "UPDATE Books SET status = \"$status\",  converted = UTC_TIMESTAMP() WHERE storage_key = \"$storageKey\"";
        if(!($result = mysql_query($query))) 
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Query failed: $query.\n" . mysql_error());
            return false;
        }
        mysql_close($link);
        return true;
    }
    
    // Updade status
    function updateBookCounter($storageKey)
    {
        if(!($link = mysql_connect($this->server, $this->user, $this->password))) 
        {
            error_log("FB2PDF ERROR. Error connecting to the database server");
            return false;
        }

        if(!mysql_select_db($this->name))
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Error selecting database");
            return false;
        }

		$set = @mysql_query ('SET NAMES UTF8');
		$set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');
        
        $query = "UPDATE Books SET counter = counter + 1 WHERE storage_key = \"$storageKey\"";
        if(!($result = mysql_query($query))) 
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Query failed: $query.\n" . mysql_error());
            return false;
        }
        mysql_close($link);
        return true;
    }
    
    // Delete book
    function deleteBook($storageKey)
    {
        if(!($link = mysql_connect($this->server, $this->user, $this->password))) 
        {
            error_log("FB2PDF ERROR. Error connecting to the database server");
            return false;
        }

        if(!mysql_select_db($this->name))
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Error selecting database");
            return false;
        }

        $query = "DELETE FROM Books WHERE storage_key = \"$storageKey\"";
        if(!($result = mysql_query($query))) 
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Query failed: $query.\n" . mysql_error());
            return false;
        }
        
        mysql_close($link);
        return true;
    }
    
    // Get list of books
    function getBooks($number)
    {
        if(!($link = mysql_connect($this->server, $this->user, $this->password))) 
        {
            error_log("FB2PDF ERROR. Error connecting to the database server");
            return false;
        }

        if(!mysql_select_db($this->name))
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Error selecting database");
            return false;
        }

		$set = @mysql_query ('SET NAMES UTF8');
		$set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');
        
        $query = "SELECT * FROM Books WHERE status = \"r\" ORDER BY id DESC LIMIT $number";
        if(!($result = mysql_query($query))) 
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Query failed: $query.\n" . mysql_error());
            return false;
        }
        
   		$list = array();
        $count = 0;
        while($row = mysql_fetch_array($result, MYSQL_ASSOC)) 
            $list[$count++] = $row;
        mysql_free_result($result);
        
        mysql_close($link);
        return $list;
    }
    
    // Get book by md5
    function getBook($md5)
    {
        if(!($link = mysql_connect($this->server, $this->user, $this->password))) 
        {
            error_log("FB2PDF ERROR. Error connecting to the database server");
            return false;
        }

        if(!mysql_select_db($this->name))
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Error selecting database");
            return false;
        }

		$set = @mysql_query ('SET NAMES UTF8');
		$set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');
        
        $query = "SELECT * FROM Books WHERE md5_hash = 0x$md5 LIMIT 1";
        if(!($result = mysql_query($query))) 
        {
            mysql_close($link);
            error_log("FB2PDF ERROR. Query failed: $query.\n" . mysql_error());
            return false;
        }
        
   		$list = array();
        if($row = mysql_fetch_array($result, MYSQL_ASSOC)) 
            $list = $row;
        mysql_free_result($result);
        
        mysql_close($link);
        return $list;
    }
}    
?>