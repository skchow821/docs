PYTHON = python
PDFLATEX = pdflatex
PRODUCTS = products
SHELL = /bin/sh

text: main.py resume.yaml contactinfo.yaml
	$(PYTHON) main.py -i resume.yaml -c contactinfo.yaml --template templates -o $(PRODUCTS)

TEX = $(pathsubst %, $(PRODUCTS)/%, $(wildcard $(PRODUCTS)/*.tex))
	
$(PRODUCTS)/%.pdf: %.tex
	$(PDFLATEX) -output-directory=$(PRODUCTS) $<

# pdf: text
#	$(PDFLATEX) -output-directory=$(PRODUCTS) $(PRODUCTS)/*.tex
