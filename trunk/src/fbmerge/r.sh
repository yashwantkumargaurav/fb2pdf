#!/bin/sh
rm -f ~/tmp/fb2mergedata/kuprin.fb2 ~/tmp/fb2mergedata/kuprin.tex ~/tmp/fb2mergedata/kuprin.pdf
./fbmerge.py -v -o ~/tmp/fb2mergedata/kuprin.fb2 ~/tmp/fb2mergedata/*xml ~/tmp/fb2mergedata/*fb2

fb2tex -v -f ~/tmp/fb2mergedata/kuprin.fb2 -o ~/tmp/fb2mergedata/kuprin.tex
(cd ~/tmp/fb2mergedata/; pdflatex kuprin.tex; pdflatex kuprin.tex)
open ~/tmp/fb2mergedata/kuprin.pdf