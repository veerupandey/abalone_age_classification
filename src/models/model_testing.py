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
    data_file : string
        Path to test data
    out_dir : string
        Path to directory where the test result should be saved
    """
    test_df = pd.read_csv(data_file + "/test.csv")
    best_model = pickle.load(open(out_dir + "/best_model.sav", "rb"))

    # show the score of best model on test data
    result = test_model(best_model, test_df)
    
    # show the coefficients of best model
    coeff_plot(best_model, out_dir)

    
def test_model(best_model, data_file):
    """test the model on test dataset
    Parameters
    ----------
    best_model : sav file
        the best ML model we have trained
    data_file : string
        Path to test data
    Returns
    -------
    float
        score
    """
    X_test = test_df.drop(columns=['Is old'])
    y_test = test_df['Is old']
    return best_model.score(X_test, y_test)

def coeff_plot(best_model, out_dir):
    """output tables and plots
    Parameters
    ----------
    best_model : sav file
        the best ML model we have trained
    out_dir : string
        Path to directory where the test result should be saved
    """
    
    feature_names = np.array(best_model[:-1].get_feature_names_out())
    coeffs = best_model.named_steps["logisticregression"].coef_.flatten()
    coeff_df = pd.DataFrame(coeffs, index=feature_names, columns=["Coefficient"])
    coeff_df_sorted = coeff_df.sort_values(by="Coefficient", ascending=False)
    dfi.export(coeff_df_sorted, out_dir + "/coeff_sorted.png")
    mglearn.tools.visualize_coefficients(coeffs, feature_names, n_top_features=5)
    plt.savefig(out_dir + "/coeff_bar.png")

if __name__ == "__main__":
    main(opt["--train_file"], opt["--out_dir"])