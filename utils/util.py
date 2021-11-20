import yaml
import logging
import os
from functools import reduce
from IPython.display import display as _display
import pandas as pd


def get_config(key=None, config_file="configs/config.yaml"):
    """
    Read the configuration file and return value of the key if present

    Args:
        key (str): Access specified key values (Format: "foo.bar.z")

    Returns:
        conf: Value for the specified key else dictionary of config_file contents
    """
    global yaml
    with open(config_file, "r") as conf:
        try:
            conf = yaml.safe_load(conf)
        except yaml.YAMLError as err:
            print("Error reading config file: {}".format(err))
    if key:
        conf = reduce(lambda c, k: c[k], key.split("."), conf)
    return conf


def display(df, n_rows=20, cache=True):
    """Display a pandas dataframe"""
    if isinstance(df, pd.DataFrame):
        df_display = df.head(n_rows)
    else:
        raise NotImplementedError(
            f"Must pass a Pandas dataframe. " f"Got {type(df)} instead"
        )

    _display(df_display)


def get_logger(file_path="", file_name=""):
    """
    This function initialize the log file

    Parameters
    ----------
    file_path: path were the logs are stored
    file_name: name of the log file

    Returns
    -------
    log: log configuration
    """
    logging.getLogger("py4j").setLevel(logging.ERROR)
    log = logging.getLogger("main_logger")
    log.setLevel("INFO")

    # log = spark._jvm.org.apache.log4j.LogManager.getLogger('main_logger')
    # log.setLevel(spark._jvm.org.apache.log4j.Level.INFO)

    # Create file handler
    logger_filepath = os.path.join(file_path, file_name)
    os.makedirs(file_path, exist_ok=True)  # create folder if needed
    fh = logging.FileHandler(logger_filepath)
    fh.setLevel("INFO")

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel("INFO")

    # Add formatter to the handlers
    formatter = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)
    return log
