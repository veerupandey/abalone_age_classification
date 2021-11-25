# author: DSCI_522_group_28
# date:

"""This script constructs various exploratory data visualizations,
and tables.

Usage: eda.py --data_path=<data_path> --outputfile=<outputfile>

Options:
--data_pathf=<data_path>          The path to read the data in from.
--output=<output>                 The path to save the images to.
"""

# import relevant modules
from docopt import docopt
import numpy as np
import pandas as pd
from altair_saver import save
import altair as alt
from sklearn.model_selection import train_test_split
import os

opt = docopt(__doc__)


def main(data_path, outputfile):
    """Calls all functions to create the exploratory data visualizations from
    the training data and saves them as png files at a specified location.

    Parameters
    __________
    train_path : str
      Path that reads in the training data.
    outputfile: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """

    # read in the full data.
    full_df = pd.read_csv(
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
        ],
        header=0,
    )

    # split the data into train and test sets
    train_df, test_df = train_test_split(full_df, test_size=0.2, random_state=123)

    # convert target from a numerical variable into a caetegorical variable
    train_df["Is old"] = np.where(train_df["Rings"] > 11, "old", "young")

    # If a directory path doesn't exist, create one
    if not os.path.exists(os.path.dirname(outputfile)):
        os.makedirs(os.path.dirname(outputfile))

    # Creates and saves figure showing distribution of target classes
    get_target_distribution(train_df, outputfile)

    # Obtains distribution of numerical variables
    get_histograms(train_df, outputfile)

    # Obtains correlation map
    get_correlation_map(train_df, outputfile)


def get_target_distribution(train_df, outputfile):
    """Obtains the distribution of target classes as a bar chart
    and saves the figure as a png file at a specified location.

    Parameters
    __________
    train_df : pd.DataFrame
      Training data as a pandas dataframe.
    outputfile: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """

    # creates the distribution of target classes as a bar chart
    distribution = (
        alt.Chart(train_df)
        .mark_bar()
        .encode(x=alt.X("count()", title="Count"), y=alt.Y("Is old"))
    )

    # saves the target class distribution figure at the specified location as target_distribution.png
    save(distribution, outputfile + "/target_distribution.png")


def get_histograms(train_df, outputfile):
    """Obtains the distributions of the numerical features as a histogram
    and saves the figure as a png file at a specified location

    Parameters
    __________
    train_df : pd.DataFrame
      Training data as a pandas dataframe.
    outputfile: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """

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
    path = os.path.join(outputfile, "histograms.png")
    # Saves the histogram at the specified location as histograms.png
    save(histogram, outputfile + "/histograms.png")


def get_correlation_map(train_df, outputfile):
    """Obtains the correlations between all numerical features and the target
    as a correlation map and saves the figure as a png at the specified location

    Parameters
    __________
    train_df : pd.DataFrame
      Training data as a pandas dataframe.
    outputfile: str
      Path where the figure should be saved.

    Returns
    _______
    None
    """

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
    save(correlation_map, outputfile + "/correlation_map.png")


if __name__ == "__main__":
    data_path = opt[--data_path]
    output_file = opt[--output_file]
    main(data_path, output_file)
