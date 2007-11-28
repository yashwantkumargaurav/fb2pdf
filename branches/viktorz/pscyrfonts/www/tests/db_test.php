<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
<?php
require_once 'awscfg.php';
require_once 'db.php';

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
    print_r($arr);
    print("<br>");
}

$letters = $db->getAuthorsFirstLetters();
print("<br><b>Authors First Letter:</b><br>");
print_r($letters);
print("<br>");

print("<br><b>Authors:</b><br>");
foreach ($letters as $l)
{
    $authors = $db->getAuthorsByFirstLetter($l);
    print_r($authors);
    print ("<br>");
}



die;

for ($i = 0; $i < $COUNT; $i++)
    $db->deleteBook("stkey$i");
?>
</body>
</html>