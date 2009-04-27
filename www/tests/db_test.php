<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
<?php
require_once 'awscfg_test.inc';
require_once '../db.php';

global $dbServer, $dbName, $dbUser, $dbPassword;

$db = new DB($dbServer, $dbName, $dbUser, $dbPassword);

$COUNT = 30;

$test_add = true;

if ($test_add)
{
    for ($i = 0; $i < $COUNT; $i++)
    {
        if ($i % 3 == 0)
            $author = "A_LastName $i, FirstName $i";
        else if ($i % 3 == 1)
            $author = "B_LastName $i, FirstName $i";
        else
            $author = "C_LastName $i, FirstName $i";
        
        $title  = "Book title $i";
        $isbn = ($i % 2 == 0) ? "123" : NULL;
        $db->insertBook("stkey$i", $author, $title, $isbn, md5("$i"), "p");
    }

    for ($i = 0; $i < $COUNT; $i++)
    {
        $status = ($i % 2 == 0) ? "r" : "e";
        $db->updateBookStatus("stkey$i", $status, 3.14);
        if ($status == "r")
            $db->updateBookCounter("stkey$i");
    }
    $db->updateBookCounter("nonexistingkey");

    $arr = $db->getBooks($COUNT);
    print("<br><b>Books:</b><br>");
    if(count($arr)==0)
    {
        print("No books!\n");
    } else
    {
        foreach($arr as $a)
        {
            print(">>> $a\n");
        }
    }
    print("<br>");
}

$letters = $db->getAuthorsFirstLetters();
print("<br><b>Authors First Letter:</b><br>");
if(count($letters)==0)
{
    print("No letters!\n");
} else
{
    foreach($letters as $a)
    {
        print(">>> $a\n");
    }

    print("<br><b>Authors:</b><br>");
    foreach ($letters as $l)
    {
        $authors = $db->getAuthorsByFirstLetter($l);
        if(count($authors)==0)
        {
            print("No authors for '%l'!\n");
        } else
        {
            foreach($authors as $a)
            {
                print(">>> $a\n");
            }
        }
        print ("<br>");
    }
}
print("<br>");


for ($i = 0; $i < $COUNT; $i++)
    $db->deleteBook("stkey$i");
?>
</body>
</html>