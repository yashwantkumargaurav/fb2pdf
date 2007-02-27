# Makefile 

allfb := $(wildcard *.fb2)
allpdf := $(patsubst %.fb2,%.pdf,$(wildcard *.fb2))
alltex := $(patsubst %.fb2,%.tex,$(wildcard *.fb2))

PDFLATEXFLAGS = -halt-on-error -interaction batchmode -no-shell-escape 

all: $(allpdf)

%.pdf: %.tex
	pdflatex $(PDFLATEXFLAGS) $<
	pdflatex $(PDFLATEXFLAGS) $<

%.tex: %.fb2
	../src/fb2tex.py -v -f $< -o $@

clean:
	rm -f *.pdf enc* *.out *.dvi *.ps *.log *.toc *.aux *.tex
