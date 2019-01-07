SHELL := /bin/sh
PYTHON := python
PDFLATEX := pdflatex
PRODUCTS := products
NAME := "Sunny_Chow"
SHA := $$(git rev-parse --short HEAD)
PDF = $(patsubst %.tex, %.pdf, $(wildcard $(PRODUCTS)/*.tex))
	
%.pdf: %.tex
	$(PDFLATEX) -output-directory=$(PRODUCTS) $<

text: main.py resume.yaml contactinfo.yaml
	$(PYTHON) main.py -i resume.yaml -c contactinfo.yaml --template templates -o $(PRODUCTS);

all: text $(PDF)
	# Rename all created pdfs to $(NAME)_$(SHA)_$(template).pdf
	for file in $(PDF); do \
		cp $$file $(PRODUCTS)/$(NAME)_$(SHA)_$$(basename $$file); \
	done

clean:
	rm -rf $(PRODUCTS)

