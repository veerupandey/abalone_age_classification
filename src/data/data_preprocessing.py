# author: Lynn Wu
# date: 2021-11-23

"""Perform train/test split and preprocess data from the downloaded csv data.
Usage: data_preprocessing.py [--url=<url>] [--outputfile_train=<outputfile_train>] [--outputfile_test=<outputfile_test>]
Options:
[--inputfile=<inputfile>]       Input path where the data is saved locally.
[--outputfile_train=<outputfile_train>]     Output path to save the preprocessed training data locally.
[--outputfile_test=<outputfile_test>]     Output path to save the preprocessed test data locally.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.compose import (
    ColumnTransformer,
    make_column_transformer
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    cross_validate,
    train_test_split,
)


from docopt import docopt
import traceback
import logging as logger
import sys

# from utils.util import get_config

def preprocess_data(inputfile, outputfile_train, outputfile_test):
    """Perform data preprocessing on the input data set.
    Parameters
    ----------
    inputfile : str
        Input file where raw data is saved.
    outputfile_train : str
        Output file to save the preprocessed training data.
    outputfile_test : str
        Output file to save the preprocessed test data.
    Returns
    -------
    None
    """
    logger.info(f"Loading data from {inputfile}")
    logger.info(f"Destination file: {outputfile_train} and {outputfile_test}")

    # Read in raw data and add column names
    column_names = ['Sex', 'Length', 'Diameter', 'Height', 'Whole weight', 
    'Shucked weight', 'Viscera weight', 'Shell weight' , 'Rings']

    df = pd.read_csv(inputfile, header=column_names)
    
    # Data wrangling on rings column to make it a categorical variable
    df['Is old'] = np.where(df['Rings'] > 11, "old", "young")

    # Split data into train/test sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)
    X_train = train_df.drop(columns=['Is old'])
    X_test = test_df.drop(columns=['Is old'])

    y_train = train_df['Is old']
    y_test = test_df['Is old']

    # Create preproceser to perform OHE on Sex feature 
    # and StandardScaler transformation on other numerical features
    categorical_feature = ['Sex']
    numerical_features = ['Length', 'Diameter', 'Height', 'Whole weight', 
    'Shucked weight', 'Viscera weight', 'Shell weight']
    target = 'Is old'
    drop_feature = ['Rings']

    preprocessor = make_column_transformer(
    (StandardScaler(), numerical_features),
    (OneHotEncoder(handle_unknown="ignore", sparse=False), categorical_feature),
    ("drop", drop_feature),
)

    preprocessor.fit(X_train, y_train)
    
    # Transformed column names
    new_columns = (
    numerical_features
    + list(
        preprocessor.named_transformers_["onehotencoder"].get_feature_names_out(
            categorical_feature
        )
    )
)
    # Fit preprocessor on training data
    X_train_enc = pd.DataFrame(
    preprocessor.transform(X_train), index=X_train.index, columns=new_columns
)
    # Combine explanatory columns with target variable into one data frame
    frames_train = [X_train_enc, y_train]
    result_train = pd.concat(frames_train)

    # Use preprocessor to transform on test data
    X_test_enc = pd.DataFrame(
    preprocessor.transform(X_test), index=X_test.index, columns=new_columns
)
    # Combine explanatory columns with target variable into one data frame
    frames_test = [X_test_enc, y_test]
    result_test = pd.concat(frames_test)

    # Write training and test data into output file paths
    result_train.to_csv(outputfile_train, index=False)
    result_test.to_csv(outputfile_test, index=False)

    logger.info(f"Training data successfully written to {outputfile_train}")
    logger.info(f"Test data successfully written to {outputfile_test}")

    if __name__ == "__main__":

        # Parse command line arguments
        opt = docopt(__doc__)

        # Preprocess the data
        inputfile = opt["--inputfile"]
        outputfile_train = opt["--outputfile_train"] # training data
        outputfile_test = opt["--outputfile_test"] # test data
        preprocess_data(inputfile, outputfile_train, outputfile_test)