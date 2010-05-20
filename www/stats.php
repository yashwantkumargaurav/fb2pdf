<?php
require_once 'utils.php';
require_once 'db.php';
require_once 'process.php';
require_once 'book_status.php';

try
{
    // get book info
    $db = getDBObject();
    $fstats = $db->getFormatStats($key);
    $furl = NULL;
    
    if($fstats)
    {
        $ctotal = 0;
        $count = count($fstats);
        for ($i = 0; $i < $count ; $i++)
        {
            $formatCount = $fstats[$i]["count"];
            $ctotal = $ctotal+$formatCount;
        }
        $cvalues=array();
        $clabels=array();
        $clegends=array();
        for ($i = 0; $i < $count ; $i++)
        {
            $formatTitle = $fstats[$i]["title"];
            $formatCount = $fstats[$i]["count"];
            $formatPC = round((100.0*$formatCount)/$ctotal);
            
            $cvalues[] = $formatCount;
            $clabels[] = $formatPC;
            $clegends[] = $formatTitle;
        }
        $furl = "http://chart.apis.google.com/chart?cht=p&chs=800x300" .
        "&chd=t:" . implode(",",$clabels) .
        "&chl=". urlencode(implode("|",$clegends));
        "&chdl=". urlencode(implode("|",$clabels));
    }

}
catch(Exception $e)
{
    error_log("FB2PDF ERROR. Status: " . $e->getMessage()); 
    httpResponseCode("400 Bad Request", $e->getMessage());
}
    
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="alternate" type="application/atom+xml" title="Atom" href="atom.php" />
<title>FB2PDF Statistics</title>
<?php include 'searchstyle.inc.php'; ?>
<?php include 'analytics.inc.php'; ?>
</head>

<body>
<h1>FB2PDF Statistics</h1>

<h2>Last month</h2>
<h3>Formats</h3>
<?php
if($furl)
    echo "<img src=\"$furl\"/>";
?>
<h3>Books Converted</h3>
<table border="1">
<tr><th>Format</th><th>Books convered</th><th>%</th></tr>
<?php
if($fstats)
{
    $count = count($fstats);
    for ($i = 0; $i < $count ; $i++)
    {
        $formatTitle = $fstats[$i]["title"];
        $formatCount = $fstats[$i]["count"];
        $formatPC = round((100.0*$formatCount)/$ctotal);
        echo "<tr>\n";
        echo "<td>". htmlspecialchars($formatTitle) . "</td>";
        echo "<td>$formatCount</td>";
        echo "<td>$formatPC%</td>";
        echo "</tr>\n";
    }
}
?>
</table>

</body>
</html>
