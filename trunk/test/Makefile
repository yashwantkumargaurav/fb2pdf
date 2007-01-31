# Makefile 

T2AENC=/sw/share/texmf-dist/source/latex/t2/enc-maps/encfiles/t2a.enc

all: test_opt.pdf

# --- TeX->DVI->PS->PDF way --
#test.dvi: test.tex 
#	latex test.tex
#	latex test.tex

#test.ps: test.dvi
#	dvips -o test.ps -Ppdf -tletter -G0 -j0 test.dvi
#	#dvips -o test.ps -Ppdf -t9cm,12cm -G0 -j0 test.dvi

#test.pdf: test.ps
#	ps2pdf -dSubsetFonts=true -dEmbedAllFonts=true test.ps

# --- PDFLatex way --
test.pdf: test.tex
	latex test.tex
	pdflatex test.tex

test_opt.pdf: test.pdf
	pdfopt test.pdf test_opt.pdf

run: test_opt.pdf
	open test_opt.pdf

clean:
	rm -f test.pdf test_opt.pdf test.dvi test.ps *.log *.toc *.aux 
