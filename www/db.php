<?php
// Helper function to create DB object (see db.php)
function getDBObject()
{
    global $dbServer, $dbName, $dbUser, $dbPassword;
    return new DB($dbServer, $dbName, $dbUser, $dbPassword);
}

// DB class
class DB
{
    var $server;
    var $name;
    var $user;
    var $password;

    var $link;
    var $result;
    
    function DB($server, $name, $user, $password) 
    {
        $this->server   = $server;
        $this->name     = $name;
        $this->user     = $user;
        $this->password = $password;
        
        $this->link     = NULL;
        $this->result   = NULL;
    }
    
    // Insert a new book
    //TODO: need to pass FORMAT parameter
    function insertBook($storageKey, $author, $title, $isbn, $md5, $status)
    {
        if (!$this->_connect())
            return false;
            
        $storageKey = mysql_real_escape_string($storageKey);
        $author     = mysql_real_escape_string($author);
        $title      = mysql_real_escape_string($title);
        $isbn       = mysql_real_escape_string($isbn);
        $status     = mysql_real_escape_string($status);
        $md5        = mysql_real_escape_string($md5);

        //TODO: change
        $query = "INSERT INTO Books (storage_key, author, title, isbn, md5hash, status, converted) 
            VALUES(\"$storageKey\", \"$author\", \"$title\", \"$isbn\", \"$md5\", \"$status\",  UTC_TIMESTAMP())";
        if (!$this->_execQuery($query))
            return false;
        
        $this->_freeQuery();
        return true;
    }
    
    // Updade status
    //TODO: need to pass FORMAT parameter
    function updateBookStatus($storageKey, $status, $ver)
    {
        if (!$this->_connect())
            return false;
            
        $storageKey = mysql_real_escape_string($storageKey);
        $status     = mysql_real_escape_string($status);
        $ver        = mysql_real_escape_string($ver);
        
        //TODO: change
        $query = "UPDATE Books SET status = \"$status\",  conv_ver = $ver, converted = UTC_TIMESTAMP() WHERE storage_key = \"$storageKey\"";
        if (!$this->_execQuery($query))
            return false;
        
        $this->_freeQuery();
        return true;
    }
    
    // Updade status
    //TODO: need to pass FORMAT parameter
    function updateBookCounter($storageKey)
    {
        if (!$this->_connect())
            return false;
            
        $storageKey = mysql_real_escape_string($storageKey);
        
        //TODO: change
        $query = "UPDATE Books SET counter = counter + 1 WHERE storage_key = \"$storageKey\"";
        if (!$this->_execQuery($query))
            return false;
        
        $this->_freeQuery();
        return true;
    }
    
    // Delete book
    function deleteBook($storageKey)
    {
        if (!$this->_connect())
            return false;
            
        $storageKey = mysql_real_escape_string($storageKey);
        
        $query = "DELETE FROM OriginalBooks WHERE storage_key = \"$storageKey\"";
        if (!$this->_execQuery($query))
            return false;
        
        $this->_freeQuery();
        return true;
    }
    
    // Get list of books
    function getBooks($number)
    {
        if (!$this->_connect())
            return false;

        //TODO: this query does not use indices! Needs to be optimized
        $query = "SELECT DISTINCT author, title, storage_key" . 
        " FROM OriginalBooks b JOIN ConvertedBooks c ON b.id=c.book_id AND status = \"r\"" .
        " ORDER BY b.id DESC LIMIT $number"
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list[$count++] = $row;
        
        $this->_freeQuery();
        return $list;
    }
    
    // Get list of books by author.
    // if number == 0, no limit
    function getBooksByAuthor($author, $number)
    {
        if (!is_numeric($number))
            return false;
            
        if (!$this->_connect())
            return false;
            
        $author = mysql_real_escape_string($author);

        //TODO: this query does not use indices! Needs to be optimized
        $query = "SELECT DISTINCT title, storage_key FROM OriginalBooks b".
        " JOIN ConvertedBooks c ON b.id=c.book_id AND status = \"r\"" .
        " WHERE author=\"$author\" ORDER BY title DESC"
        if ($number > 0)
            $query = $query . " LIMIT $number";
            
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list[$count++] = $row;
        
        $this->_freeQuery();
        return $list;
    }
    
    // Get list of books by author.
    // if number == 0, no limit
    function getBooksByAuthorRSS($author, $number)
    {
        if (!is_numeric($number))
            return false;
            
        if (!$this->_connect())
            return false;
            
        $author = mysql_real_escape_string($author);
        
        $query = "SELECT * FROM Books WHERE author = \"$author\" AND status = \"r\" ORDER BY id DESC";
        if ($number > 0)
            $query = $query . " LIMIT $number";
            
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list[$count++] = $row;
        
        $this->_freeQuery();
        return $list;
    }

    // Get book by key
    function getBookByKey($key)
    {
        if (!$this->_connect())
            return false;
            
        $key = mysql_real_escape_string($key);
        
        $query = "SELECT * FROM Books WHERE storage_key = \"$key\" LIMIT 1";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        if ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list = $row;
            
        $this->_freeQuery();
        return $list;
    }
    
    // Get book by md5
    function getBookByMd5($md5)
    {
        if (!$this->_connect())
            return false;
            
        $md5 = mysql_real_escape_string($md5);
        
        $query = "SELECT * FROM Books WHERE md5hash = \"$md5\" LIMIT 1";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        if ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list = $row;
            
        $this->_freeQuery();
        return $list;
    }
    
    // Get first letters of authors
    // Returns array where key/value is a first letter
    function getAuthorsFirstLetters()
    {
        if (!$this->_connect())
            return false;
            
        $query = "SELECT DISTINCT UPPER(LEFT(author,1)) as letter FROM Books WHERE status = \"r\"";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC))
        {        
            $letter = $row["letter"];
            $list[$letter] = $letter;
        }
            
        $this->_freeQuery();
        return $list;
    }
    
    // Get authors by first letter
    // Returns array each element of it is an array with keys "author" and "number". 
    // This array is sorted by authors.
    function getAuthorsByFirstLetter($letter)
    {
        if (!$this->_connect())
            return false;
            
        $letter = mysql_real_escape_string($letter);
        
        $query = "SELECT author, count(id) AS number FROM Books WHERE author LIKE \"$letter%\" AND status=\"r\" GROUP BY author ORDER BY author ASC";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC))
            $list[$count++] = $row;
            
        $this->_freeQuery();
        return $list;
    }
    
    // Internal methods
    function _connect()
    {
        if(!($this->link = mysql_connect($this->server, $this->user, $this->password))) 
        {
            error_log("FB2PDF ERROR. Error connecting to the database server");
            return false;
        }

        if(!mysql_select_db($this->name))
        {
            mysql_close($this->link);
            $this->link = NULL;
            error_log("FB2PDF ERROR. Error selecting database");
            return false;
        }

        $set = @mysql_query ('SET NAMES UTF8');
        $set = @mysql_query ('SET COLLATION_CONNECTION=UTF8_GENERAL_CI');

        return true;
    }
    
    function _execQuery($query)
    {
        if(!($this->result = mysql_query($query))) 
        {
            mysql_close($this->link);
            $this->link = NULL;
            error_log("FB2PDF ERROR. Query failed: $query.\n" . mysql_error());
            return false;
        }
        
        return true;
    }
    
    function _freeQuery()
    {
        if (($this->result !== true) and ($this->result !== false))
            mysql_free_result($this->result);
            
        mysql_close($this->link);
        
        $this->result = NULL;
        $this->link   = NULL;
    }
}    
?>
