# Abalone Age Classifier

Data analysis project for DSCI 522 (Data Science workflows); a course in the Master of Data Science program at the University of British Columbia.

## Authors
- Nick Lisheng Mao
- Beilin Wu (Lynn)
- Kiran Phaterpekar
- Rakesh Pandey


## Introduction
Abalones are endangered marine snails that are found in the cold coastal water around the world. The price of an abalone is positively associated with its age. However, determining how old an abalone is a very complex process. 

In this project we are classifying abalone snails into "young" and "old" according to their number of rings based on input features such as abalone's gender, height with meat in shell, weight of the shell etc.



## About Data Set and Analysis

The Abalone data set that was used in this project was sourced from the UC Irvine Machine Learning Repository published in 1995. It can be found here. Each row in the data set represents the attributes and physical measurements of abalones including number of rings, sex, length, diameter, height, weight, etc. The number of rings were counted manually using a microscope by the researchers. The age of an abalone is represented by its number of rings plus 1.5 as number of years lived. The data set has already removed its missing values and the range of the continuous values have been scaled for use with an ANN (by dividing by 200).

In the research paper "A Quantitative Comparison of Dystal and Backpropagation" that David Clark, Zoltan Schreter and Anthony Adams submitted to the Australian Conference on Neural Networks (ACNN'96), the original abalone data set was treated as a 3-category classification problem (grouping ring classes 1-8, 9 and 10, and 11 on). In our project, we will treat the data set as a 2-categorical classification problem (grouping ring classes less or equal to 11, and more than 11).

Here, we aim to answer one research question with a Logistic Regression classification model:

**Given the input features (sex, longest shell measurement, diameter perpendicular to length, height with meat in shell, whole weight, weight of meat, gut weight after bleeding, shell weight after being dried), is an abalone young (i.e. number of rings smaller than or equal to 11), or old (i.e. number of rings is larger than 11)?**

To perform this analysis, first, after the data download, we split the data into train set and test set, perform data wrangling, and perform EDA on the train set features to investigate the relationships between the independent variables used in our model. We then preprocess the data including scaling the numerical features and one-hot-encoding the categorical feature. Next, we fit a Logistic Regression classification model on the data set, tune hyperparameters and evaluate the best performing model on the test set. The final step is creating a full report that shares the analysis results, as structured below.


## Report

The final report can be found <a href="https://github.com/UBC-MDS/abalone_age_classification/blob/main/docs/Project_report_milestone2.ipynb" >here</a>. The final analysis report consists of the following components: summary, introduction, methods including data and analysis, results/discussion, future analysis directions/takeaway and references.

## Usage

### Create project evironment

Project `python` environment needs to be created before running the analysis. Run the command mentioned below from project root directory.

```bash
conda env create -f environment.yml
conda activate abalone
```

### Run analysis end to end

To run the analysis end to end, run the script `runner.sh` in a Terminal/Command Prompt from the project root directory as follows. Script `runner.sh` runs each individual script one at a time.

```bash
nohup bash runner.sh > runner.log &
```

### (Optional) Run individual script

To run modules individually, please follow the instructions below. All the scripts should be run from project root directory.

#### 1. Download the data

To download the data, run the command as follows..

```bash
python src/data/data_download.py --url="https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data" --outputfile="data/raw/abalone.data"
```

#### 2. Data prerocessing

Run the data preprocessing script as follows.

```bash
python src/data/data_preprocessing.py --inputfile="data/raw/abalone.data" --out_dir="data/processed"
```

#### 3. Exploratory data analysis (EDA)

Script `src/eda/eda.py` generates EDA reports and save it to the specified location.

```bash
python src/eda/eda.py --data_path="data/processed/train.csv" --out_dir="results/eda"
```

#### 4. Train the model

To train the model, run the script `src/models/train.py` as follows.

```bash
python src/models/train.py --data_file="data/processed/train.csv" --out_dir="results/model"
```

#### 5. Test and evaluate model performance

To generate the model test and evaluation report, run the script `src/models/test.py`.

```bash
python src/models/test.py --data_file="data/processed/test.csv" --out_dir="results/model"
```

#### 6. Build the report

Our final analysis report is published as jupyter book and available in directory `docs`.

To create the contents of jupyter book, execute the command mentioned below.

```bash
jupyter-book build docs
```

#### 7. Publish the report

Reports can be published as github pages. 

URL should start with the username. Example:-

`https://<username>.github.io/abalone_age_classification/README.html`

To publish the report, run the command mentioned below.

```bash
ghp-import -n -p -f docs/_build/html
```

Our report for this anlysis is available [here](https://UBC-MDS.github.io/abalone_age_classification/README.html).


**_Note:_** If a script runs without command line arguments, arguments will be fetched from `configs/config.yaml` file.

## Dependencies

A environment file `environment.yml` of dependencies can be found <a href="https://github.com/UBC-MDS/abalone_age_classification/blob/main/environment.yml">here</a>. As project develops, this `yaml` file is subjected to change.

## Explanatory Data Analysis
A detailed EDA report can be found <a href="https://github.com/UBC-MDS/abalone_age_classification/blob/main/src/eda/eda.ipynb" >here</a>.

## License

This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. This allows for the sharing and adaptation of the datasets for any purpose, provided that the appropriate credit is given.


## References

```{bibliography} references.bib
:all:
```
