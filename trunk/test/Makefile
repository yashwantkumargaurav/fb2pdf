# Makefile 

all: test_opt.pdf biykov_orfografiya_opt.pdf

test.pdf: test.tex
	pdflatex test.tex
	pdflatex test.tex

test_opt.pdf: test.pdf
	pdfopt test.pdf test_opt.pdf

biykov_orfografiya_opt.pdf: biykov_orfografiya.pdf
	pdfopt biykov_orfografiya.pdf biykov_orfografiya_opt.pdf

biykov_orfografiya.pdf: biykov_orfografiya.tex
	pdflatex biykov_orfografiya.tex
	pdflatex biykov_orfografiya.tex

biykov_orfografiya.tex: biykov_orfografiya.fb2 ../src/*.py
	../src/fb2tex.py -f biykov_orfografiya.fb2 -o biykov_orfografiya.tex

run: test_opt.pdf
	open test_opt.pdf

runb: biykov_orfografiya_opt.pdf
	open biykov_orfografiya_opt.pdf

clean:
	rm -f test.pdf test_opt.pdf *.out *.dvi *.ps *.log *.toc *.aux biykov_orfografiya_opt.pdf biykov_orfografiya.pdf biykov_orfografiya.tex
