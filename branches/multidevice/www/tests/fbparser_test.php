<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
<?php
require_once 'fbparser.php';

$fb = new FBParser();
if (!$fb->parse("test.fb2"))
    die ("error parsing fb2");

print ("<br>Title = " . $fb->getTitle());
print ("<br>Name = " . $fb->getAuthor());

?>
</body>
</html>