<?php
function menu_item($name, $url, $title, $text)
{
    global $active_menu;
    
    if ($name == $active_menu)
    {
        $menuClass = "menu_active";
    }
    else
    {
        $menuClass = "menu";
    }
    
    if (!$url)
        $url = '#';
        
    echo "<li class=\"$menuClass\">";
    echo "<a href=\"$url\" title=\"$title\"><span style=\"cursor:pointer\">$text</span></a>";
    echo "</li>";
}
?>

<div id="menu"> 
    <div class="tabsC">
        <ul>
            <?php 
            menu_item('main', 'index.php', 'Главная', '&nbsp;Главная&nbsp;'); 
            menu_item('about', 'about.php', 'О сервисе', 'О сервисе&nbsp;'); 
            menu_item('store', 'store.php', 'Магазин', '&nbsp;Магазин&nbsp;'); 
            menu_item('library', 'library.php', 'Библиотека', 'Библиотекa'); 
            menu_item('faq', 'faq.php', 'FAQ', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FAQ&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'); 
            ?>
        </ul>
    </div>
</div>
