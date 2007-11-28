#!/bin/sh

rsync -avz --exclude=.svn www/ codeminders.com:~/public_html/fb2pdf/
ssh codeminders.com "chmod a+rx ~/public_html/fb2pdf/; chmod a+r ~/public_html/fb2pdf/*"

