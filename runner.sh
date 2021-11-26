
#!/usr/bin/env bash
# Script: runner.sh
# DSCI_522_GROUP28, Nov 2021
#
# runner.sh script executes all the steps needed 
# to run and reproduce abalone age classifier.
# 
# Usage: bash runner.sh

# Download data
python  src/data/data_download.py  --url="https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data" --outputfile="data/raw1/abalone.data"

# Data preprocessing
python src/data/data_preprocessing.py --inputfile="data/raw/abalone.data" --out_dir="data/processed"

# EDA
python src/eda/eda.py --data_path="data/processed/train.csv" --out_dir="reports/eda"