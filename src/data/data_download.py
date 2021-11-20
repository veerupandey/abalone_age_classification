# author: Rakesh Pandey
# date: 2021-11-19

"""Downloads data from a web url.
Usage: data_download.py [--url=<url>] [--outputfile=<outputfile>]

Options:
[--url=<url>]                   Web URL for the csv file.
[--outputfile=<outputfile>]     Output path to save the data locally.
"""

# Import all the modules from project root directory
from pathlib import Path
import sys

project_root = str(Path(__file__).parents[2])
sys.path.append(project_root)


# Import relevant modules
import os
import traceback
import requests
import pandas as pd
from docopt import docopt

# Custom imports
from utils.util import get_config, get_logger

# Define logger
logger = get_logger()


def get_data(url, outputfile):
    """Download the data from the url and save it to disk.

    Parameters
    ----------
    url : int
        Web URL to download data.
    outputfile : str
        Output file to save the data on disk.

    Returns
    -------
    None
    """

    logger.info(f"Dowloading data from {url}")
    logger.info(f"Destination file: {outputfile}")
    try:
        request = requests.get(url, allow_redirects=True)
        assert request.status_code == 200
    except Exception as req:
        logger.info("Error! Please see the details below.")
        traceback.print_exc()

    # Read data from the url as pandas df
    df = pd.read_csv(url, header=None)

    # Create the path if not exists
    if not os.path.exists(os.path.dirname(outputfile)):
        os.makedirs(os.path.dirname(outputfile))

    # Write csv to file
    df.to_csv(outputfile, index=False)

    logger.info(f"File successfully written to {outputfile}")


if __name__ == "__main__":

    # Parse command line arguments
    opt = docopt(__doc__)

    # # Download data
    url = opt.get("--url")
    outputfile = opt.get("--outputfile")

    # if optional arguments are not provided
    # read it from config file
    if not url:
        url = get_config("data.url")

    if not outputfile:
        outputfile = os.path.join(project_root, get_config("data.outputfile"))

    # Get data
    get_data(url, outputfile)
