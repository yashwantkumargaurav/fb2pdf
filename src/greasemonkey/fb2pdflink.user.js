// Hello World! example user script
// version 0.1
// 2007-08-22
// Copyright (c) 2005, Vadim Zaliva
// Released under the GPL license
// http://www.gnu.org/copyleft/gpl.html
//
// --------------------------------------------------------------------
//
// This is a Greasemonkey user script.
//
// To install, you need Greasemonkey: http://greasemonkey.mozdev.org/
// Then restart Firefox and revisit this script.
// Under Tools, there will be a new menu item to "Install User Script".
// Accept the default configuration and install.
//
// To uninstall, go to Tools/Manage User Scripts,
// select "Hello World", and click Uninstall.
//
// --------------------------------------------------------------------
//
// ==UserScript==
// @name          fb2pdf
// @namespace     http://codeminders.com/fb2pdf/
// @description   Suppliment links to .fb2 files with links to .pdf files for SonyReader converted via FB2PDF converter
// @include       *
// @exclude       http://codeminders.com/*
// @exclude       http://www.codeminders.com/*
// @exclude       http://www.diveintogreasemonkey.org/*
// ==/UserScript==

var replaceLinks = function() {
    var allLinks, thisLink;
    allLinks = document.evaluate(
        "//a[@href]",
        document,
        null,
        XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
        null);
    for (var i = 0; i < allLinks.snapshotLength; i++) {
        thisLink = allLinks.snapshotItem(i);
        if(thisLink.href.match(/^http:\/\/.*\.fb2$/i) || thisLink.href.match(/^http:\/\/.*\.fb2\.zip$/i)) {
            //alert("link"+thisLink);
            newElement = document.createElement('span');
            postUrl = 'http://www.codeminders.com/fb2pdf/convert.php?url=' + encodeURIComponent(thisLink.href);
            newElement.innerHTML='&nbsp[<a target=\'_blank\' href="' + postUrl + '">SonyReader PDF</a>]';
            thisLink.parentNode.insertBefore(newElement, thisLink.nextSibling);
        }
    }
}

window.addEventListener('load',  replaceLinks, true);
