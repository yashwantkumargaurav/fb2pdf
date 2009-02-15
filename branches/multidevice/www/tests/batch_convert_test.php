<html>

<script type="text/javascript">
count = 1;
function add()
{
    count++;
    var bname = "book" + count;
    document.getElementById("urls").innerHTML += 
        '<input type="text" name="' + bname +'" size="48"><br>'; 
}
</script>

<body>

<p>Batch convert test</p>
<form id="uploadform" enctype="multipart/form-data" action="../batch_convert.php" method="POST">
    <div id="urls">
    <input type="text" name="book1" size="48"><br>
    </div>
    <a href="javascript:add()">Add</a><br>
    <input type="submit" value="submit">
</form>

</body>
</html>
