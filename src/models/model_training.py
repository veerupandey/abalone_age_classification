# author: Nick
# date: 2021-11-25

"""Fit a logistic regression based on input train data.
Save the models and coefficients in a table as png.
Usage: model_analysis.py [--data_file=<data_file>] [--out_dir=<out_dir>]
Options:
[--data_file=<data_file>]        Data set file path while train and test data are saved as csv.
[--out_dir=<out_dir>]            Output path to save model, tables and images.
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
    """run all helper functions to find the best model and get the 
    hyperparameter tuning result
    Parameters
    ----------
    input_file : string
        the path (including file name) to the training dataset
    out_dir : string
        the path to store the results
    """
    train_df = pd.read_csv(data_file + "/train_df.csv")
    best_ridge, result_df = best_model(train_df)

    # save the best model
    pickle.dump(best_model, open(out_dir + "/best_model.sav", "wb"))

    # save the hyperparameter tuning plot
    train_plot(train_results, out_dir + "cv_result.png")
    

def build_pipe():

    """build a logistic regression pipeline with column transformer
    to preprocess every column

    Returns
    -------
    sklearn.pipeline.Pipeline
        ML pipeline
    """

    # build column transformer
    categorical_feature = ['Sex']
    numerical_features = ['Length', 'Diameter', 'Height', 'Whole weight', 
                          'Shucked weight', 'Viscera weight', 'Shell weight']
    target = 'Is old'
    drop_feature = ['Rings']

    preprocessor = make_column_transformer(
        (StandardScaler(), numerical_features),
        (OneHotEncoder(handle_unknown="ignore", sparse=False), 
         categorical_feature),
        ("drop", drop_feature),
    )

    # build pipe line
    lr = LogisticRegression(max_iter=2000)
    pipe = make_pipeline(preprocessor, lr)

    return pipe


def best_model(data_file):
    """Train the logistic model by using random search
    with cross validation
    
    Parameters
    ----------
    train_file : string
        Train data set file path, including filename

    Returns
    -------
    train_results: dataframe
        A data frame with train score results from each model
    """
    # split train data for cross validation
    train_df = pd.read_csv(data_file + "/train.csv")
    X_train = train_df.drop(columns=['Is old'])
    y_train = train_df['Is old']
    
    # set parameter grid
    param_grid = {"logisticregression__C": 10.0 ** np.arange(-3, 4)}
    
    # fit model
    random_search = RandomizedSearchCV(build_pipe(),
                                       param_distributions = param_grid,
                                       n_jobs = -1,
                                       n_iter = 10,
                                       cv = 5,
                                       random_state = 123)
    random_search.fit(pd.DataFrame(X_train), y_train)
    
    # create output dataframe
    train_results = pd.DataFrame(random_search.cv_results_)[
    [   "mean_test_score",
        "param_logisticregression__C",
        "mean_fit_time",
        "rank_test_score",
        ]
    ].set_index("rank_test_score").sort_index()
    
    # find the best model
    best_model = random_search.best_estimator_
    
    return best_model, train_results


def train_plot(train_results, out_dir):
    """Save the parameter vs score plot from train results
    Parameters
    ----------
    result_df : pandas.core.frame.DataFrame
        a dataframe contains hyper parameters and scores
    out_dir : string
        the path to store the plot
    """
    train_results.plot(x = "param_logisticregression__C", y = "mean_test_score")
    plt.xscale("log")
    plt.savefig(out_dir)

if __name__ == "__main__":
    main(opt["--train_file"], opt["--out_dir"])
