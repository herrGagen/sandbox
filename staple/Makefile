all: thesis.pdf presentation.pdf

watch: thesis.tex
	echo latexmk -pvc -view=pdf $< 

%.tex: 
	echo "$@ being made from makefile"

thesis.pdf: thesis.tex  abstract.tex intervals.tex airplane.tex waiter1D.tex intervalsBody.tex airplaneBody.tex waiter1DBody.tex intervalPapers.bib airplanePapers.bib waiterPapers.bib Makefile
		latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make $<

Zuber.pdf: Zuber.tex intervals.pdf airplane.pdf waiter1D.pdf intervalPapers.bib airplanePapers.bib waiterPapers.bib Makefile
		latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make $<

%.pdf: %.tex %Body.tex Makefile mystyle.sty
	latexmk -f -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make $<



clean: 
	latexmk -CA
	rm -rf \#* *~ *.bbl *.log *.aux *.nav *.snm
