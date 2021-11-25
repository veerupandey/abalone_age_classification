# author: DSCI_522_group_28
# date:

"""This script constructs various exploratory data visualizations,
and tables.
Usage: eda.py [--data_path=<data_path>] [--out_dir=<out_dir>]

Options:
[--data_path=<data_path>]          The path to read the data in from.
[--out_dir=<out_dir>]                The path to save the images to.
"""
# Import all the modules from project root directory
from pathlib import Path
import sys

project_root = str(Path(__file__).parents[2])
sys.path.append(project_root)

# import relevant modules
from docopt import docopt
import numpy as np
import pandas as pd
import altair as alt
from sklearn.model_selection import train_test_split
import os

# Customer imports
from utils.util import get_config, get_logger

# Define logger
logger = get_logger()


def main(data_path, out_dir):
    """Calls all functions to create the exploratory data visualizations from
    the training data and saves them as png files at a specified location.

    Parameters
    __________
    train_path : str
      Path that reads in the training data.
    out_dir: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """

    # read in the full data.
    train_df = pd.read_csv(
        data_path,
        names=[
            "Sex",
            "Length",
            "Diameter",
            "Height",
            "Whole weight",
            "Shucked weight",
            "Viscera weight",
            "Shell weight",
            "Rings",
            "Is old",
        ],
        header=0,
    )

    # If a directory path doesn't exist, create one
    os.makedirs(out_dir, exist_ok=True)

    # Creates and saves figure showing distribution of target classes
    get_target_distribution(train_df, out_dir)

    # Obtains distribution of numerical variables
    get_histograms(train_df, out_dir)

    # Obtains correlation map
    get_correlation_map(train_df, out_dir)


def get_target_distribution(train_df, out_dir):
    """Obtains the distribution of target classes as a bar chart
    and saves the figure as a png file at a specified location.

    Parameters
    __________
    train_df : pd.DataFrame
      Training data as a pandas dataframe.
    out_dir: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """
    logger.info("Running get_target_distribution...")

    # creates the distribution of target classes as a bar chart
    distribution = (
        alt.Chart(train_df)
        .mark_bar()
        .encode(x=alt.X("count()", title="Count"), y=alt.Y("Is old"))
    )

    # saves the target class distribution figure
    # at the specified location as target_distribution.png
    path = os.path.join(out_dir, "target_distribution.png")
    distribution.save(path)
    logger.info(f"Distribution chart successfully saved to {path}")


def get_histograms(train_df, out_dir):
    """Obtains the distributions of the numerical features as a histogram
    and saves the figure as a png file at a specified location

    Parameters
    __________
    train_df : pd.DataFrame
      Training data as a pandas dataframe.
    out_dir: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """

    logger.info("Running get_histograms...")

    # creates the distribution for each numerical feature for both target classes
    histogram = (
        alt.Chart(train_df)
        .mark_bar(opacity=0.4)
        .encode(
            x=alt.X(alt.repeat(), type="quantitative", bin=alt.Bin(maxbins=50)),
            y=alt.Y("count()", stack=None),
            fill="Is old",
        )
        .repeat(
            [
                "Length",
                "Diameter",
                "Height",
                "Whole weight",
                "Shucked weight",
                "Viscera weight",
                "Shell weight",
            ],
            columns=2,
        )
    )

    # Saves the histogram at the specified location as histograms.png
    path = os.path.join(out_dir, "histograms.png")
    histogram.save(path)
    logger.info(f"Histogram chart successfully saved to {path}")


def get_correlation_map(train_df, out_dir):
    """Obtains the correlations between all numerical features and the target
    as a correlation map and saves the figure as a png at the specified location

    Parameters
    __________
    train_df : pd.DataFrame
      Training data as a pandas dataframe.
    out_dir: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """

    logger.info("Running get_correlation_map...")

    # determine correlation values between each numerical feature/target
    corr_df = (
        train_df.drop(["Sex", "Is old"], axis=1)
        .corr("spearman")
        .abs()
        .stack()
        .reset_index(name="corr")
    )

    # create correlation map
    correlation = (
        alt.Chart(corr_df)
        .mark_rect()
        .encode(
            x=alt.X("level_0", title=None),
            y=alt.Y("level_1", title=None),
            color=alt.Color("corr"),
        )
        .properties(height=300, width=300)
    )

    # add labels for each correlation value
    correlation_map = correlation + correlation.mark_text().encode(
        text=alt.Text("corr", format=",.2r"), color=alt.value("black")
    )

    # saves the correlation map at a specified location as correlation_map.png
    path = os.path.join(out_dir, "correlation_map.png")
    correlation_map.save(path)
    logger.info(f"Correlation chart successfully saved to {path}")


if __name__ == "__main__":

    # Parse command line parameters
    opt = docopt(__doc__)

    data_path = opt["--data_path"]
    out_dir = opt["--out_dir"]

    # Read it from config file
    # if command line arguments are missing
    if not data_path:
        data_path = os.path.join(project_root, get_config("eda.data_path"))

    if not out_dir:
        out_dir = os.path.join(project_root, get_config("eda.out_dir"))

    # Run the main function
    logger.info("Running eda...")
    main(data_path, out_dir)
    logger.info("EDA script successfully completed. Exiting!")
