# author: Lynn Wu
# date: 2021-11-23

"""Preprocess data from the downloaded csv data.
Usage: data_preprocessing.py [--url=<url>] [--outputfile=<outputfile>]
Options:
[--inputfile=<inputfile>]       Input path where the data is saved locally.
[--outputfile=<outputfile>]     Output path to save the preprocessed data locally.
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

def preprocess_data(inputfile, outputfile):
    """Perform data preprocessing on the input data set.
    Parameters
    ----------
    inputfile : str
        Input file where raw data is saved.
    outputfile : str
        Output file to save the preprocessed data.
    Returns
    -------
    None
    """
    logger.info(f"Loading data from {inputfile}")
    logger.info(f"Destination file: {outputfile}")

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

    preprocessor.fit(X_train)
    
    # Transformed column names
    new_columns = (
    numeric_features
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
    frames_train = [X_train_enc, y_train]
    result_train = pd.concat(frames_train)

    # Fit preprocessor on test data
    preprocessor.fit(X_test)

    X_test_enc = pd.DataFrame(
    preprocessor.transform(X_test), index=X_test.index, columns=new_columns
)
    frames_test = [X_test_enc, y_test]
    result_test = pd.concat(frames_test)

    # TBD: write training and test data into output file path...
    # result_train.to_csv(outputfile, index=False)
    # result_test.to_csv(outputfile, index=False)

    if __name__ == "__main__":

    # Parse command line arguments
    opt = docopt(__doc__)

    # Download data
    inputfile = opt["--inputfile"]
    outputfile = opt["--outputfile"] # train
    outputfile = opt["--outputfile"] # test
    preprocess_data(inputfile, outputfile)