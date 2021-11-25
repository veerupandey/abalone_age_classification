# author: Lynn Wu
# date: 2021-11-25

"""Cleans and performs train/test split from the downloaded csv data.
Usage: src/data_preprocessing.py [--url=<url>] [--out_dir=<out_dir>]
Options:
[--inputfile=<inputfile>]       Input path where the data is saved locally.
[--out_dir=<out_dir>]     Output path to save the training and test data locally.
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

def main(inputfile, out_dir):
    """Perform data wrangling and train/test splitting on the input data set.
    Parameters
    ----------
    inputfile : str
        Input file where raw data is saved.
    out_dir : str
        Output diredctory to save the training and test data.
    Returns
    -------
    None
    """
    logger.info(f"Loading data from {inputfile}")
    logger.info(f"Destination folder: {out_dir}")

    # Read in raw data and add column names
    column_names = ['Sex', 'Length', 'Diameter', 'Height', 'Whole weight', 
    'Shucked weight', 'Viscera weight', 'Shell weight' , 'Rings']

    df = pd.read_csv(inputfile, header=column_names)
    
    # Data wrangling on rings column to make it a categorical variable
    df['Is old'] = np.where(df['Rings'] > 11, "old", "young")
    df = df.drop(columns = "Rings")

    # Split data into train/test sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)

    # Write training and test data into output directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    train_df.to_csv(out_dir + '/training.csv')
    logger.info(f"Training data successfully saved to {out_dir}")

    test_df.to_csv(out_dir + '/test.csv')
    logger.info(f"Test data successfully saved to {out_dir}")

    # Run the main function
    if __name__ == "__main__":
        logger.info("Running data_preprocessing.py...")
        main(inputfile, out_dir)
        logger.info("Training and test csv successfully saved!")