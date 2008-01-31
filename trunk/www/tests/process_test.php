<html>
<body>
<?php
require_once '../process.php';

try
{
    $p = new ConvertBook();
    $p->convertFromUrl("http://google.com");
    print ("OK");
}
catch (Exception $e)
{
    print ($e->getCode() . " - " . $e->getMessage());
}
?>
</body>
</html>