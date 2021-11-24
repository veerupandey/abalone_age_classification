# author: DSCI_522_group_28
# date: 

'''This script constructs various exploratory data visualizations,
and tables.

Usage: eda.py --train_path=<train_path> --outputfile=<outputfile>

Options:
--train_pathf=<train_path>
--output=<output>
'''


from docopt import docopt 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os

opt = docopt(__doc__)

def main(train_path, outputfile):
  
  
  df = pd.read_csv("../../data/raw/abalone.data")
  
  train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)
  # If a directory path doesn't exist, create one
 # if not os.path.exists(os.path.dirname(outputfile)):
  #      os.makedirs(os.path.dirname(outputfile)) 
        
  # Develop human-readable column names
  
  
  # Develop and save summary statistic table
  
  # Creates figure showing distribution of target classes and categorical features
  
  # Obtains distribution of numerical variables
  
  # Obtains correlation map
    
  pass

def get_summary_table():
  pass

def get_target_distribution():
  pass

def get_violin_plots():
  pass

def get_correlation_map():
  pass

#if __name__ == "__main__":
  #main(opt[--train_path], opt[--output_file])
  
df = pd.read_csv('../../data/raw/abalone.data')
train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)
