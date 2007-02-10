# Makefile 

all: test_opt.pdf

test.pdf: test.tex
	latex test.tex
	pdflatex test.tex

test_opt.pdf: test.pdf
	pdfopt test.pdf test_opt.pdf

run: test_opt.pdf
	open test_opt.pdf

clean:
	rm -f test.pdf test_opt.pdf test.dvi test.ps *.log *.toc *.aux 
