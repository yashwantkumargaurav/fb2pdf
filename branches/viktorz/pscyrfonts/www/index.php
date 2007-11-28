<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="alternate" type="application/atom+xml" title="Atom" href="atom.php" />
<title>Конвертор FictionBook2 в PDF для Sony Reader</title>
<?php include 'analytics.inc.php'; ?>

<script type="text/javascript">
function toggleUploadMode(file) 
{
    if (file) 
    {
        document.getElementById('upfile').style.display='block';
        document.getElementById('upurl').style.display='none';
    } 
    else 
    {
        document.getElementById('upfile').style.display='none';
        document.getElementById('upurl').style.display='block';
    }
 }
 
function doUpload()
{
    // hide form
    document.getElementById('container').style.display = 'none';
    // show progress indicator
    document.getElementById('progress').style.display = '';
    // submit form
    document.getElementById('uploadform').submit();
    // hack for IE: when form is submitted, IE stops to load and animate pictures 
    // so we'll ask IE to show picture again _AFTER_ form submission, with some delay (200ms)
    setTimeout('showProgress()', 200);
}

function showProgress()
{
    // refresh image source to start animation
    var o = document.getElementById('pimage');
    if (o)
        o.src = 'images/progress.gif';
}

function showForm()
{
    // hide progress indicator
    document.getElementById('progress').style.display = 'none';
    // show form
    document.getElementById('container').style.display = '';
}

function selectText(source)
{
    if (source)
    {   
        source.focus();
        source.select();
    }
}

</script>
</head>
<body>

<?php
$url = (isset($_GET["url"])) ? $_GET["url"] : NULL;
?>

<center>
<div id="container" class="WidthPage">
    <?php 
    include 'header.inc.php'; 
    $active_menu = 'main';
    include 'menu.inc.php'; 
    ?>
    
    <div id="tab_box">
        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
        <div class="tab_box_content">
            <div id="convert_box">
            <div id="more_news"><a href="news.php"><u>Все новости</u></a></div>
            <p class="news"><span class="light_green">Новость:</span>&nbsp;&nbsp;<span class="green">07.08.2007</span>&nbsp;&nbsp;--&nbsp;&nbsp;
            Новый дизайн сайта. Добавлена библиотека.</p>
                <b class="ctop"><b class="cb1"></b><b class="cb2"></b><b class="cb3"></b><b class="cb4"></b></b>
                <div class="conv_box_content">
                    <div id="intro">
                        <div id="width480">
                        <div class="roundedcornr_box_fr">
                        <div class="roundedcornr_top_line_fr"><div class="roundedcornr_top_fr"><div></div></div></div>
                        <div class="roundedcornr_left_line_fr">
                            <div class="roundedcornr_content_fr">
                            <p class="justify">Пожалуйста загрузите книгу в FB2 или ZIP формате (ZIP может содержать только одну книгу в FB2 формате) или укажите URL.</p>
                    
                    <form id="uploadform" enctype="multipart/form-data" action="uploader.php" method="POST">
                            <input type="radio" class="red_line" name="uploadtype" value="file" onclick="toggleUploadMode(true);" <?php if (!$url) print "checked" ?> /> Файл
                            <input type="radio" name="uploadtype" value="url" onclick="toggleUploadMode(false);" <?php if ( $url) print "checked" ?> /> URL
                            
                            <div id="upfile" class="upfield" <?php if ($url) print 'style="display: none"' ?>>
                                <input type="file" name="fileupload" id="fileupload" size="25"/>
                            </div> 
                            
                            <div id="upurl" class="upfield" <?php if (!$url) print 'style="display: none"' ?>>
                                <input type="text" id="fileupload" value="<?php print ($url) ? $url : "наберите URL здесь" ?>" name="url" size="30" onclick="selectText(this);"/>
                            </div>
                            
                            </div><!--end roundedcornr_content_fr-->
                            <div class="roundedcornr_bottom_line_fr"><div class="roundedcornr_bottom_fr"><div></div></div></div>
                        </div><!--roundedcornr_left_line_fr-->
                        </div><!--end roundedcornr_box_fr-->
                        
                        <div id="arrow"><img src="images/arrow.gif" alt="arrow"/></div>
                        </div> <!-- width480-->	
                        
                        <div id="email_div">
                            <p class="left"> email (не обязательно):    
                            <input type="text" id="email" value="" name="email" size="30"/>
                            </p>
                            
                            <p class="justify"><span class="small">Вы можете указать адрес Вашей электронной почты, и мы пошлём Вам письмо, 
                            как только книга будет готова.
                            <span class="grey">Введённый Вами адрес используется <u>только</u> для уведомления о готовности книги.              
                            Мы гарантируем конфидeнциальность, и обязуемся <u>не использовать</u> указанный Вами адрес для рассылки рекламы.   
                            </span></span>
                            </p>
                        </div><!--email_div-->
                    </div> <!--intro-->  
                    
                    <div id="sony_reader">
                        <img src="images/sony_reader.jpg" alt="sony reader"/>
                        <input id="ConvertBtnUpld" style="margin: 5px 0px 0px 0px;"
                            onmouseup  ="this.src='images/button.gif'" 
                            onmousedown="this.src='images/button_pressed.gif'"
                            onmouseover="this.src='images/button_active.gif'" 
                            onmouseout ="this.src='images/button.gif'"
                            onclick    ="doUpload();" 
                            type="image" src="images/button.gif" />
                    </div>
                    </form>
                </div> <!--end of convert box content-->	
            <b class="cbottom"><b class="cb4"></b><b class="cb3"></b><b class="cb2"></b><b class="cb1"></b></b>
            </div>  <!--end of convert box -->
            
            <div id="more_books"><a href="library.php"><u>Все книги</u></a></div>
            <h4>Книги, сконвертированные недавно:</h4> 
            <img src="images/green_px.gif" class="line"/>

            <?php
            require_once 'awscfg.php';
            require_once 'db.php';
            require_once 'utils.php';

            global $awsS3Bucket;
            global $dbServer, $dbName, $dbUser, $dbPassword;
            
            // list of new books
            $MAX_BOOKS = 40;
            $MAX_ROWS  = 20;
            $MAX_COLS  = 2;
            
            $db = new DB($dbServer, $dbName, $dbUser, $dbPassword);
            $list = $db->getBooks($MAX_BOOKS);
            if ($list)
            {
                $count = count($list);
                for ($col = $MAX_COLS - 1; $col >= 0 ; $col--)
                {
                    if ($col == 0)
                        echo '<div class="left_book">';
                    else
                        echo '<div class="right_book">';
                    
                    for ($row = 0; $row < $MAX_ROWS; $row++)
                    {
                        $i = $col * $MAX_ROWS + $row;
                        if ($i < $count)
                        {
                            $author = $list[$i]["author"];
                            $title  = $list[$i]["title"];
                            $key    = $list[$i]["storage_key"];
                            if (strrpos($key, ".") === false) // old style key (no extension)
                                $key = $key . ".pdf";

                            if (!$author)
                                $author = "Автор неизвестен";
                            if (!$title)
                                $title = "Название неизвестно";
                            
                            echo "$author&nbsp;&nbsp;<a href=\"getfile.php?key=$key\">\"$title\"</a><br/>";
                        }
                    }
                    echo '</div>';
                }
            }
            ?>

            <img src="images/green_px.gif" class="line"/>
            <?php include 'footer.inc.php'; ?>

        </div>  <!--end of tab box content-->	
        <b class="xbottom"><b class="xb4"></b><b class="xb3"></b><b class="xb2"></b><b class="xb1"></b></b>
    </div> <!--end of tab box -->
<br/>
<br/>
</div> <!--end of container-->

<!-- div to display progress indicator --> 
<div id="progress" style="display:none;text-align:center">
    <h4 align="center">Загрузка файла. Пожалуйста, подождите...</h4>
    <img id="pimage" src="images/progress.gif" alt="progress bar"/>
</div>

</center>
</body>
</html>
 