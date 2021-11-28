
#!/usr/bin/env bash
# Script: runner.sh
# DSCI_522_GROUP28, Nov 2021
#
# runner.sh script executes all the steps needed 
# to run and reproduce abalone age classifier.
# 
# Usage: bash runner.sh

# Download data
echo "Downloading data"
python  src/data/data_download.py  --url="https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data" --outputfile="data/raw/abalone.data"

# Data preprocessing
echo "Running data preprocessing script"
python src/data/data_preprocessing.py --inputfile="data/raw/abalone.data" --out_dir="data/processed"

# EDA
echo "Running eda script"
python src/eda/eda.py --data_path="data/processed/train.csv" --out_dir="results/eda"

# Train
echo "Running training script"
python src/models/train.py --data_file="data/processed/train.csv" --out_dir="results/model"

# Test
echo "Running test script"
python src/models/test.py --data_file="data/processed/test.csv" --out_dir="results/model"

# Run jupyter book
jupyter-book build docs

# Publish jupyter book on github pages
ghp-import -n -p -f docs/_build/html

echo "Exiting! Script successfully completed."