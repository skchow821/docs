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

# Forces a reevaluation of $(PDF) after files have been generated.  It's pretty ugly.
# May rewrite this to include the actual templates + source files... 
# https://stackoverflow.com/questions/49286398/defer-prerequisite-expansion-until-after-a-different-target-creation
ifndef expand-prereq
all: text
	$(MAKE) --no-print-directory -f $(lastword $(MAKEFILE_LIST)) $@ expand-prereq=y
else 
all: text $(PDF)
	for file in $(PDF); do \
		cp $$file $(PRODUCTS)/$(NAME)_$(SHA)_$$(basename $$file); \
	done
endif

clean:
	rm -rf $(PRODUCTS)

