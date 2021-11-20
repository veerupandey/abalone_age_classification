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
