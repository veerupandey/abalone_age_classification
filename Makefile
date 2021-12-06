# This is a makefile to automate the project abalone_age_classification.
# Author: DSCI_522_group_28

## ----------------------------------------------------------------------
## Usage: make [target]
## Passing 'all' as the target will reproduce the analysis end to end.
## Passing 'clean' will clean all the analysis output files.
## Conda environment can be created with target 'create_env'.
## However, it must be activated in the terminal before running make.
## Passing 'format' as the target will format the code in src directory.
## ----------------------------------------------------------------------

.PHONY: create_env format clean data 

#################################################################################
# COMMANDS TO RUN ANALYSIS                                                                     #
#################################################################################

# Publish report webpage locally
all: data/raw/abalone.data data/processed/train.csv data/processed/test.csv \
	results/eda results/model docs/_build publish_local

all_git_publish: data/raw/abalone.data data/processed/train.csv data/processed/test.csv \
	results/eda results/model docs/_build publish

## Set up python interpreter environment
create_env:
	conda env create -f environment.yml

## Download Data
data/raw/abalone.data: src/data/data_download.py
	python  src/data/data_download.py  \
	--url="https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data" \
	--outputfile="data/raw/abalone.data"

## Data preprocessing
data/processed/train.csv data/processed/test.csv: data/raw/abalone.data src/data/data_preprocessing.py	
	python src/data/data_preprocessing.py --inputfile="data/raw/abalone.data" --out_dir="data/processed"

## EDA
results/eda: data/processed/train.csv src/eda/eda.py
	python src/eda/eda.py --data_path="data/processed/train.csv" --out_dir="results/eda"


##  Model output
results/model: data/processed/train.csv data/processed/test.csv src/models/train.py src/models/test.py
	python src/models/train.py --data_file="data/processed/train.csv" --out_dir="results/model"
	python src/models/test.py --data_file="data/processed/test.csv" --out_dir="results/model"

## Jupyter book
docs/_build: results/eda results/model 
	jupyter-book build docs

publish: docs/_build
	ghp-import -n -p -f docs/_build/html

publish_local: docs/_build
	cd docs/_build/html && python -m http.server

#################################################################################
# DEVOPS COMMANDS                                                               #
#################################################################################

# Create flow chart
flowchart:
	make -Bnd | make2graph | dot -Tpng -o results/images/flowchart.png

## Format using black formatter
format:
	black src

# Docker build
docker_build: Dockerfile
	docker build -t  abalone_age_classification .

## Clean environment
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf data/raw/*
	rm -rf data/processed/*
	rm -rf results/eda/*
	rm -rf results/model/*
	rm -rf docs/_build


help: 
	@echo "usage: make [target] ..."
	@echo ""

#################################################################################
# END
#################################################################################
