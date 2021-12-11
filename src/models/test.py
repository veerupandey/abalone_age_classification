# author: Nick
# date: 2021-11-25

"""Test the best model on test dataset.
Save the coefficient bar plot as png.
Usage: test.py [--data_file=<data_file>] [--out_dir=<out_dir>]

Options:
[--data_file=<data_file>]        Data set file test data are saved as csv.
[--out_dir=<out_dir>]            Output path to save results, tables and images.
"""

import os
import sys
from pathlib import Path

project_root = str(Path(__file__).parents[2])
sys.path.append(project_root)

from docopt import docopt
import matplotlib.pyplot as plt
import mglearn
from mglearn.plot_2d_separator import (plot_2d_separator, plot_2d_classification,
                                plot_2d_scores)
from mglearn.plot_helpers import cm2 as cm, discrete_scatter

import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import get_scorer

# Customer imports
from utils.util import get_config, get_logger

# Define logger
logger = get_logger()


def main(data_file, out_dir):
    """load the best model and fit on test data
    Parameters
    ----------
    data_file : string
        Path to test data
    out_dir : string
        Path to directory where the test result should be saved
    """

    test_df = pd.read_csv(data_file)
    best_model = pickle.load(open(out_dir + "/best_model.sav", "rb"))

    # show the score of best model on test data in a table
    result = test_model(best_model, test_df)

    # show the coefficients of best model
    coeff_plot(best_model, out_dir)


def test_model(best_model, test_df):
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
    logger.info("Testing on test set...")
    scoring_metrics = [
        "accuracy",
        "f1",
        "recall",
        "precision",
        "roc_auc",
        "average_precision",
    ]
    X_test = test_df.drop(columns=["Is old"])
    y_test = test_df["Is old"]
    y_test = y_test.map({"young": 1, "old": 0}).astype(int)

    rdf = pd.DataFrame(scoring_metrics, columns=["Metrics"])

    r = []
    for m in scoring_metrics:
        r.append(get_scorer(m)(best_model, X_test, y_test))
    rdf["Test Result"] = r
    rdf.set_index("Metrics")
    rdf.to_html(os.path.join(out_dir, "test_result_table.html"), escape=False)
    logger.info("Test set results saved as a table")


def coeff_plot(best_model, out_dir):
    """output tables and plots
    Parameters
    ----------
    best_model : sav file
        the best ML model we have trained
    out_dir : string
        Path to directory where the test result should be saved
    """
    logger.info("Drawing bar plot for coefficents...")
    feature_names = np.array(best_model[:-1].get_feature_names_out())
    coeffs = best_model.named_steps["logisticregression"].coef_.flatten()
    coeff_df = pd.DataFrame(coeffs, index=feature_names, columns=["Coefficient"])
    coeff_df_sorted = coeff_df.sort_values(by="Coefficient", ascending=False)
    coeff_df_sorted.to_html(os.path.join(out_dir, "coeff_sorted.html"), escape=False)
    visualize_coefficients(coeffs, feature_names, n_top_features=5)
    plt.savefig(os.path.join(out_dir, "coeff_bar.png"), bbox_inches = 'tight')
    logger.info("Bar plot for coefficents saved")

    
def visualize_coefficients(coefficients, feature_names, n_top_features=25):
    """Visualize coefficients of a linear model.
    Parameters
    ----------
    coefficients : nd-array, shape (n_features,)
        Model coefficients.
    feature_names : list or nd-array of strings, shape (n_features,)
        Feature names for labeling the coefficients.
    n_top_features : int, default=25
        How many features to show. The function will show the largest (most
        positive) and smallest (most negative)  n_top_features coefficients,
        for a total of 2 * n_top_features coefficients.
    """
    coefficients = coefficients.squeeze()
    if coefficients.ndim > 1:
        # this is not a row or column vector
        raise ValueError("coeffients must be 1d array or column vector, got"
                         " shape {}".format(coefficients.shape))
    coefficients = coefficients.ravel()

    if len(coefficients) != len(feature_names):
        raise ValueError("Number of coefficients {} doesn't match number of"
                         "feature names {}.".format(len(coefficients),
                                                    len(feature_names)))
    # get coefficients with large absolute values
    coef = coefficients.ravel()
    positive_coefficients = np.argsort(coef)[-n_top_features:]
    negative_coefficients = np.argsort(coef)[:n_top_features]
    interesting_coefficients = np.hstack([negative_coefficients,
                                          positive_coefficients])
    # plot them
    plt.figure(figsize=(15, 5))
    colors = [cm(1) if c < 0 else cm(0)
              for c in coef[interesting_coefficients]]
    plt.bar(np.arange(2 * n_top_features), coef[interesting_coefficients],
            color=colors)
    feature_names = np.array(feature_names)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(np.arange(0, 2 * n_top_features),
               feature_names[interesting_coefficients], rotation=60,
               ha="right")
    plt.ylabel("Coefficient magnitude")
    plt.xlabel("Feature")

    
if __name__ == "__main__":

    # Parse command line parameters
    opt = docopt(__doc__)

    data_file = opt["--data_file"]
    out_dir = opt["--out_dir"]

    # Read it from config file
    # if command line arguments are missing
    if not data_file:
        data_file = os.path.join(project_root, get_config("model.test.data_file"))

    if not out_dir:
        out_dir = os.path.join(project_root, get_config("model.test.out_dir"))

    # Run the main function
    logger.info("Running testing...")
    main(data_file, out_dir)
    logger.info("Test script successfully completed. Exiting!")
