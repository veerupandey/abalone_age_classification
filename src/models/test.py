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
import numpy as np
import pandas as pd
import dataframe_image as dfi
import pickle

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

    # show the score of best model on test data
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
    logger.info("Drawing bar plot for coefficents...")
    feature_names = np.array(best_model[:-1].get_feature_names_out())
    coeffs = best_model.named_steps["logisticregression"].coef_.flatten()
    coeff_df = pd.DataFrame(coeffs, index=feature_names, columns=["Coefficient"])
    coeff_df_sorted = coeff_df.sort_values(by="Coefficient", ascending=False)
    dfi.export(coeff_df_sorted, out_dir + "/coeff_sorted.png")
    mglearn.tools.visualize_coefficients(coeffs, feature_names, n_top_features=5)
    plt.savefig(out_dir + "/coeff_bar.png")


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
