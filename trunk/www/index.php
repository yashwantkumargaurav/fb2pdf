<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>FictionBook2 to PDF file converter</title>
<script type="text/javascript">
function toggleuploadmode(file) {
    if (file) {
        document.getElementById('upfile').style.display='block';
        document.getElementById('upurl').style.display='none';
    } else {
        document.getElementById('upfile').style.display='none';
        document.getElementById('upurl').style.display='block';
    }
 }
</script>
</head>
<body>
<p>Please upload your FB2 file or specify URL:
<p>

<form enctype="multipart/form-data" action="uploader.php" method="POST">

 <input type="radio" name="uploadtype" value="file" onclick="toggleuploadmode(true);" checked /> file
 <input type="radio" name="uploadtype" value="url" onclick="toggleuploadmode(false);" /> url

 <div id="upfile">
 <input type="file" name="fileupload" size="30" id="fileupload"/>
 </div>
 
 <div id="upurl" style="display: none">
 <input type="text" id="fileupload" value="type url here" name="url" size="30"/>
 </div>
 
<input type="submit" value="Upload File" />
</form>
</body>
 