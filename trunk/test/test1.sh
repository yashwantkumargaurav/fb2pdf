#!/bin/sh

# Converts single book
# Usage: test1.sh <file.fb2>

FB2FILES="*.fb2"
PDFLATEXFLAGS="-halt-on-error -interaction batchmode -no-shell-escape"
FB2TEX=../scripts/fb2tex
rm -f *.pdf enc* *.out *.dvi *.ps *.log *.toc *.aux *.tex *.fblog

PYTHONPATH=../src/
export PYTHONPATH

rsync -avz --exclude=".svn"  ../src/TeX/ ./

i=$1
echo "Processing $i"
N=`basename $i .fb2`
t=${N}.tex
echo $N
python ${FB2TEX} -v -f $i -o $t > $N.fblog 2>&1
if [ $? -ne 0 ]; then
    echo "TeX file generation failed";
else
    p=${N}.pdf
    pdflatex ${PDFLATEXFLAGS} $t $p 
    if [ $? -ne 0 ]; then
        echo "1st pass of pdflatex failed"
    else
        pdflatex ${PDFLATEXFLAGS} $t $p > /dev/null $2>1
        if [ $? -ne 0 ]; then
            echo "2nd pass of pdflatex failed"
        else
            echo "OK. Generated $t"
        fi
    fi
fi
