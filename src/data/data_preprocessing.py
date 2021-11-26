# author: Lynn Wu
# date: 2021-11-25

"""Cleans and performs train/test split from the downloaded csv data.
Usage: src/data_preprocessing.py [--inputfile=<inputfile>] [--out_dir=<out_dir>]

Options:
[--inputfile=<inputfile>]       Input path where the data is saved locally.
[--out_dir=<out_dir>]     Output path to save the training and test data locally.
"""

# Import all the modules from project root directory
from pathlib import Path
import sys

project_root = str(Path(__file__).parents[2])
sys.path.append(project_root)

# Standard import
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from docopt import docopt
import traceback
import sys

# Custom imports
from utils.util import get_config
from utils.util import get_logger

# Define logger
logger = get_logger()


def data_preprocess(inputfile, out_dir):
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
    column_names = [
        "Sex",
        "Length",
        "Diameter",
        "Height",
        "Whole weight",
        "Shucked weight",
        "Viscera weight",
        "Shell weight",
        "Rings",
    ]

    df = pd.read_csv(inputfile, skiprows=1, names=column_names)

    # Data wrangling on rings column to make it a categorical variable
    df["Is old"] = np.where(df["Rings"] > 11, "old", "young")
    # df = df.drop(columns="Rings")

    # Split data into train/test sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)

    # If a directory path doesn't exist, create one
    os.makedirs(out_dir, exist_ok=True)

    # Write training and test data into output directory
    train_path = os.path.join(out_dir, "train.csv")
    train_df.to_csv(train_path, index=False)
    logger.info(f"Training data successfully saved to {train_path}")

    test_path = os.path.join(out_dir, "test.csv")
    test_df.to_csv(test_path)
    logger.info(f"Test data successfully saved to {test_path}")


# Run the main function
if __name__ == "__main__":

    # Parse command line parameters
    opt = docopt(__doc__)

    inputfile = opt["--inputfile"]
    out_dir = opt["--out_dir"]

    # Read it from config file
    # if command line arguments are missing
    if not inputfile:
        inputfile = os.path.join(project_root, get_config("preprocess.inputfile"))

    if not out_dir:
        out_dir = os.path.join(project_root, get_config("preprocess.out_dir"))

    print(inputfile, out_dir)

    logger.info("Running data_preprocessing.py...")
    data_preprocess(inputfile, out_dir)
    logger.info("Training and test csv successfully saved!")
