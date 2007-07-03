<div id="menu"> 
    <div class="tabsC">
        <ul>
            <?php global $active_menu; ?>
            <li class=<?php print ($active_menu == 'main')    ? "menu_active" : "menu" ?>>
                <a href="index.php" title="Главная"><span>&nbsp;Главная&nbsp;</span></a>
            </li>
            <li class=<?php print ($active_menu == 'about')   ? "menu_active" : "menu" ?>>
                <a href="#" title="О сервисе"><span>О сервисе&nbsp;</span></a>
            </li>
            <li class=<?php print ($active_menu == 'store')   ? "menu_active" : "menu" ?>>
                <a href="#" title="Магазин"><span>&nbsp;Магазин&nbsp;</span></a>
            </li>
            <li class=<?php print ($active_menu == 'library') ? "menu_active" : "menu" ?>>
                <a href="library.php" title="Библиотека"><span>Библиотекa</span></a>
            </li>
            <li class=<?php print ($active_menu == 'faq')     ? "menu_active" : "menu" ?>>
                <a href="#" title="FAQ"><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FAQ&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></a>
            </li>
        </ul>
    </div>
</div>
