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
    function insertBook($storageKey, $author, $title, $isbn, $md5)
    {
        if (!$this->_connect())
            return false;
        
        $storageKey = mysql_real_escape_string($storageKey);
        $author     = mysql_real_escape_string($author);
        $title      = mysql_real_escape_string($title);
        $isbn       = mysql_real_escape_string($isbn);
        $status     = mysql_real_escape_string($status);
        $md5        = mysql_real_escape_string($md5);

        // insert into OriginalBooks
        $query = "INSERT INTO OriginalBooks (storage_key, author, title, isbn, md5hash, submitted) 
            VALUES(\"$storageKey\", \"$author\", \"$title\", \"$isbn\", \"$md5\", UTC_TIMESTAMP())";

        if (!mysql_query($query))
        {
            $this->_disconnect();
            return false;
        }
        
        $this->_disconnect();
        return true;
    }

    function insertBookFormat($storageKey, $format)
    {
        if (!is_numeric($format))
            return false;
            
        if (!$this->_connect())
            return false;
            
        $storageKey = mysql_real_escape_string($storageKey);
        $ver        = mysql_real_escape_string($ver);

        $query = "INSERT INTO ConvertedBooks (book_id, format, status) " .
            "SELECT id, $format, \"p\" FROM OriginalBooks WHERE storage_key = \"$storageKey\"";

        if (!mysql_query($query))
        {
            $this->_disconnect();
            return false;
        }
        
        $this->_disconnect();
        return true;
    }
    
    // Updade status
    function updateBookStatus($storageKey, $status, $ver, $format)
    {
        if (!is_numeric($format))
            return false;
            
        if (!$this->_connect())
            return false;
            
        $storageKey = mysql_real_escape_string($storageKey);
        $status     = mysql_real_escape_string($status);
        $ver        = mysql_real_escape_string($ver);
        
        mysql_query("BEGIN");
        
        // update ConvertedBooks status
        $query = "UPDATE ConvertedBooks SET status = \"$status\", conv_ver = $ver, converted = UTC_TIMESTAMP()" .
                 " WHERE format = $format AND book_id IN" . 
                 " (SELECT id FROM OriginalBooks WHERE storage_key = \"$storageKey\")";
        if (!mysql_query($query))
        {
            error_log("Query '$query' failed. Rolling back");
            mysql_query("ROLLBACK");
            $this->_disconnect();
            return false;
        }

        // update OrginalBooks if converted successfully
        if ($status == 'r')
        {
            $query = "UPDATE OriginalBooks SET valid = TRUE WHERE storage_key = \"$storageKey\"";
            if (!mysql_query($query))
            {
                error_log("Query '$query' failed. Rolling back");
                mysql_query("ROLLBACK");
                $this->_disconnect();
                return false;
            }
        }

        mysql_query("COMMIT");

        $this->_disconnect();
        return true;
    }
    
    // Updade status
    function updateBookCounter($storageKey, $format)
    {
        if (!is_numeric($format))
            return false;
            
        if (!$this->_connect())
            return false;
            
        $storageKey = mysql_real_escape_string($storageKey);
        
        $query = "UPDATE ConvertedBooks SET counter = counter + 1" . 
                 " WHERE format = $format AND book_id IN" .
                 " (SELECT id FROM OriginalBooks WHERE storage_key = \"$storageKey\")";
        if (!$this->_execQuery($query))
            return false;
        
        $this->_disconnect();
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
        
        $this->_disconnect();
        return true;
    }
    
    // Get list of books
    function getBooks($number)
    {
        if (!is_numeric($number))
            return false;
            
        if (!$this->_connect())
            return false;

        $query = "SELECT author, title, storage_key" . 
        " FROM OriginalBooks WHERE valid=TRUE" .
        " ORDER BY id DESC LIMIT $number";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list[$count++] = $row;
        
        $this->_disconnect();
        return $list;
    }
    
    // Get book formats
    function getBookStatus($storageKey, $format)
    {
        if (!is_numeric($format))
            return false;
            
        if (!$this->_connect())
            return false;

        $query = "SELECT status, converted, counter, conv_ver FROM ConvertedBooks " .
            " WHERE format = $format AND book_id IN" .
            " (SELECT id FROM OriginalBooks WHERE storage_key = \"$storageKey\")";
        if (!$this->_execQuery($query))
            return false;
        
        $row = mysql_fetch_array($this->result, MYSQL_ASSOC);
        
        $this->_disconnect();
        return $row;
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

        //TODO: see if we can get rid of filesort in this query
        // (see mysql EXPLAIN on it)
        $query = "SELECT title, storage_key FROM OriginalBooks ".
        " WHERE valid=TRUE" .
        " AND author=\"$author\" ORDER BY title DESC";
        if ($number > 0)
            $query = $query . " LIMIT $number";
            
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list[$count++] = $row;
        
        $this->_disconnect();
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

        $query = "SELECT id,title,author,storage_key,submitted FROM OriginalBooks WHERE author = \"$author\" AND valid=TRUE ORDER BY id DESC";
        if ($number > 0)
            $query = $query . " LIMIT $number";
            
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list[$count++] = $row;
        
        $this->_disconnect();
        return $list;
    }

    // Get book by key
    function getBookByKey($key)
    {
        if (!$this->_connect())
            return false;
            
        $key = mysql_real_escape_string($key);
        
        $query = "SELECT title,author FROM OriginalBooks WHERE storage_key = \"$key\" LIMIT 1";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        if ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list = $row;
            
        $this->_disconnect();
        return $list;
    }
    
    // Get book by md5
    function getBookByMd5($md5)
    {
        if (!$this->_connect())
            return false;
            
        $md5 = mysql_real_escape_string($md5);

        //TODO: this query does not use indices. Add indices to approriate tables.
        // see mysql EXPLAIN
        $query = "SELECT id, storage_key FROM OriginalBooks" . 
                 " WHERE md5hash = \"$md5\"";
        
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        if ($row = mysql_fetch_array($this->result, MYSQL_ASSOC)) 
            $list = $row;
            
        $this->_disconnect();
        return $list;
    }
    
    // Get first letters of authors
    // Returns array where key/value is a first letter
    function getAuthorsFirstLetters()
    {
        if (!$this->_connect())
            return false;

        //TODO: see if we can get rid of 'using temporary' here.
        // see mysql EXPLAIN
        $query = "SELECT DISTINCT UPPER(LEFT(author,1)) as letter FROM OriginalBooks WHERE valid=TRUE";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC))
        {        
            $letter = $row["letter"];
            $list[$letter] = $letter;
        }
            
        $this->_disconnect();
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
        
        $query = "SELECT author, count(id) AS number FROM OriginalBooks WHERE author LIKE \"$letter%\" AND valid=TRUE GROUP BY author ORDER BY author ASC";
        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC))
            $list[$count++] = $row;
            
        $this->_disconnect();
        return $list;
    }

    // Get list of formats
    function getFormats() 
    {
        if (!$this->_connect())
            return false;

	$query = "SELECT id, title FROM Formats ORDER BY id";

        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        $count = 0;
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC))
            $list[$count++] = $row;
            
        $this->_disconnect();
        return $list;
    }
      
    // Get list of formats
    function getFormatParameters($format) 
    {
        if (!is_numeric($format))
            return false;
            
        if (!$this->_connect())
            return false;

	$query = "SELECT name, value FROM FormatParams WHERE format = $format";

        if (!$this->_execQuery($query))
            return false;
        
        $list = array();
        while ($row = mysql_fetch_array($this->result, MYSQL_ASSOC))
        {
            $name = $row["name"];
            $value = $row["value"];
            $list[$name] = $value;
        }   
        $this->_disconnect();
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
    
    function _disconnect()
    {
        if (($this->result !== true) and ($this->result !== false)
            and ($this->result !== NULL))
            mysql_free_result($this->result);
            
        mysql_close($this->link);
        
        $this->result = NULL;
        $this->link   = NULL;
    }
}    
?>
