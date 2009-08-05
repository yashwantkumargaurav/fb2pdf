#!/bin/sh

# Script to convert single book to PDF
# Intended to be used in dev. environment for testing

PDFLATEXFLAGS="-halt-on-error -interaction batchmode -no-shell-escape"
FB2TEX=../scripts/fb2tex
rm -f *.pdf enc* *.out *.dvi *.ps *.log *.toc *.aux *.tex *.fblog

PYTHONPATH=../src/
export PYTHONPATH


usage()
{
cat << EOF
Usage: `basename $0` -f <fb2file> -o <pdfile> [-d devicetype]
EOF
}


# parse command line arguments
while getopts hf:o:d: OPT; do
    case "$OPT" in
	h)	usage
		exit 0
		;;
	f)	
        FB2FILE=$OPTARG
		;;
	o)	
        PDFFILE=$OPTARG
		;;
	d)	
        DEVTYPE=$OPTARG
		;;
	\?)	# getopts issues an error message
        echo "Unknown option: $OPTIND" >&1
		usage >&2
		exit 1
		;;
    esac
done

if [[ -z $FB2FILE ]] || [[ -z $PDFFILE ]]
then
     usage
     exit 1
fi

WORKDIR=`mktemp -d /tmp/fb2pdf.XXXXXX` || exit 1

rsync -aqz --exclude=".svn"  ../src/TeX/ $WORKDIR

TEXFILE=$WORKDIR/`basename $FB2FILE .fb2`.tex
TMPPDFFILE=$WORKDIR/`basename $FB2FILE .fb2`.pdf

if [ -z $DEVTYPE ]; then
    python ${FB2TEX} -v -f $FB2FILE -o $TEXFILE
else
    python ${FB2TEX} -v -f $FB2FILE -o $TEXFILE -p devicetype:$DEVTYPE
fi
if [ $? -ne 0 ]; then
    echo "Generating TEX file failed"
    rm -rf $WORKDIR
    exit 1
fi

ODIR=`pwd`
cd $WORKDIR
pdflatex ${PDFLATEXFLAGS} $TEXFILE $TMPPDFFILE
if [ $? -ne 0 ]; then
    echo "pdflatex failed"
    rm -rf $WORKDIR
    exit 1
fi

pdflatex ${PDFLATEXFLAGS} $TEXFILE $PDFFILE
if [ $? -ne 0 ]; then
    echo "pdflatex failed"
    rm -rf $WORKDIR
    exit 1
fi

cd $ODIR
cp $TMPPDFFILE $PDFFILE
rm -f fb2tex.log
rm -rf $WORKDIR

