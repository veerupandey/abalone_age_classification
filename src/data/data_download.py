# author: Rakesh Pandey
# date: 2021-11-19

"""Downloads data from a web url.
Usage: data_download.py [--url=<url>] [--outputfile=<outputfile>]

Options:
[--url=<url>]                   Web URL for the csv file.
[--outputfile=<outputfile>]     Output path to save the data locally.
"""

import os
import pandas as pd
import requests

from docopt import docopt
import traceback
import logging as logger
import sys

# from utils.util import get_config


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

    # Download data
    url = opt["--url"]
    outputfile = opt["--outputfile"]
    get_data(url, outputfile)
