# author: Nick
# date: 2021-11-25

"""Fit a logistic regression based on input train data.
Save the models and coefficients in a table as png.
Usage: model_testing.py [--data_file=<data_file>] [--out_dir=<out_dir>]
Options:
[--data_file=<data_file>]        Data set file path where train and test data are saved as csv.
[--out_dir=<out_dir>]            Output path to save results, tables and images.
"""

import os
import sys
import docopt
import IPython
import ipywidgets as widgets
import matplotlib.pyplot as plt
import mglearn
import numpy as np
import pandas as pd
import dataframe_image as dfi
import pickle
from IPython.display import HTML, display
from ipywidgets import interact, interactive
from sklearn.model_selection import cross_val_score, cross_validate, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
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
from sklearn.linear_model import LogisticRegression

%matplotlib inline
pd.set_option("display.max_colwidth", 200)

opt = docopt(__doc__)


def main(data_file, out_dir):
    """load the best model and fit on test data
    Parameters
    ----------
    test : string
        Path (including filename) to test data (csv file)
    out_dir : string
        Path to directory where the test result should be saved
    """
    test_df = pd.read_csv(data_file + "/test_df.csv")
    best_model = pickle.load(open(out_dir + "/best_model.sav", "rb"))

    result = test_model(best_model, test_df)

    
def test_model(best_model, test_df):
    """test the model on test dataset
    Parameters
    ----------
    (best_model : sav file
        the best ML model we have trained
    test_df : pandas.core.frame.DataFrame
        a dataframe containing test dataset
    Returns
    -------
    float
        score
    """
    X_test = test_df.drop(columns=['Is old'])
    y_test = test_df['Is old']
    return best_model.score(X_test, y_test)

def coeff_plot(best_model, ):
    