# author: Nick
# date: 2021-11-25

"""Fit a logistic regression based on input train data.
Save the models and coefficients in a table as png.
Usage: train.py [--data_file=<data_file>] [--out_dir=<out_dir>]

Options:
[--data_file=<data_file>]        Data set file train are saved as csv.
[--out_dir=<out_dir>]            Output path to save model, tables and images.
"""

# Import all the modules from project root directory
from pathlib import Path
import sys

project_root = str(Path(__file__).parents[2])
sys.path.append(project_root)

import os
from docopt import docopt
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

# Customer imports
from utils.util import get_config, get_logger

# Define logger
logger = get_logger()

def main(data_file, out_dir):
    """run all helper functions to find the best model and get the 
    hyperparameter tuning result
    Parameters
    ----------
    input_file : string
        the path to the training dataset
    out_dir : string
        the path to store the results
    """
    # If a directory path doesn't exist, create one
    os.makedirs(out_dir, exist_ok=True)
    
    train_df = pd.read_csv(data_file)
    pipe = build_pipe()
    best_model, train_results = fit_model(train_df, pipe)

    # save the best model
    pickle.dump(best_model, open(out_dir + "/best_model.sav", "wb"))

    # save the hyperparameter tuning plot
    train_plot(train_results, out_dir + "/cv_result.png")
    
    # save train results as a table
    train_df_table(train_results, out_dir)
    

def build_pipe():

    """build a logistic regression pipeline with column transformer
    to preprocess every column

    Returns
    -------
    sklearn.pipeline.Pipeline
        ML pipeline
    """

    logger.info("Building the pipeline...")

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
    
    logger.info("Successfully built the pipeline...")
    
    return pipe


def fit_model(train_df, pipe):
    """Train the logistic model by using random search
    with cross validation
    
    Parameters
    ----------
    data_file : string
        Train data set file path, including filename

    Returns
    -------
    train_results: dataframe
        A data frame with train score results from each model
    """
    
    logger.info("Fitting the model...")
    
    # split train data for cross validation
    X_train = train_df.drop(columns=['Is old'])
    y_train = train_df['Is old']
    y_train=y_train.map({'young': 1, 'old': 0}).astype(int)
    
    # set parameter grid
    param_grid = {"logisticregression__C": 10.0 ** np.arange(-3, 4)}
    
    # fit model
    random_search = GridSearchCV(pipe,
                                 param_grid = param_grid,
                                 n_jobs = -1,
                                 cv = 5)
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
    
    logger.info("Model fitted...")
    
    return best_model, train_results


def train_plot(train_results, out_dir):
    """Save the parameter vs score plot from train results
    Parameters
    ----------
    train_results : pandas.core.frame.DataFrame
        a dataframe contains hyper parameters and scores
    out_dir : string
        the path to store the plot
    """
    logger.info("Making train results plot...")
    train_results.plot(x = "param_logisticregression__C", y = "mean_test_score")
    plt.xscale("log")
    plt.savefig(out_dir)
    logger.info(f"Train results plot saved to {out_dir}")


def train_df_table(train_results, out_dir):

    logger.info("Making train results table...")
    path = os.path.join(out_dir, "train_result_table.png")
    dfi.export(train_results, path)
    logger.info(f"Train results table saved to {out_dir}")


if __name__ == "__main__":

    # Parse command line parameters
    opt = docopt(__doc__)

    data_file = opt["--data_file"]
    out_dir = opt["--out_dir"]

    # Read it from config file
    # if command line arguments are missing
    if not data_file:
        data_file = os.path.join(project_root, get_config("model.train.data_file"))

    if not out_dir:
        out_dir = os.path.join(project_root, get_config("model.train.out_dir"))

    # Run the main function
    logger.info("Running training...")
    main(data_file, out_dir)
    logger.info("Training script successfully completed. Exiting!")

