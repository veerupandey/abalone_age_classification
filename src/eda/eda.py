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
import altair as alt
import matplotlib.pyplot as plt
from altair_saver import save
from sklearn.model_selection import train_test_split
import os

opt = docopt(__doc__)

def main(train_path, outputfile):
  
  # Read in data as a dataframe
  train_df = pd.read_csv(train_path)
  
  # If a directory path doesn't exist, create one
  if not os.path.exists(os.path.dirname(outputfile)):
    os.makedirs(os.path.dirname(outputfile)) 
        
  # Develop human-readable column names
  cols = [
    "Sex",
    "Length",
    "Diameter",
    "Height",
    "Whole weight",
    "Shucked weight",
    "Viscera weight",
    "Shell weight",
    "Rings",
    "Age"
  ]
  
  # Develop and save summary statistic table
  get_summary_table(train_df, outputfile)
  
  # Creates and saves figure showing distribution of target classes
  get_target_distributions(train_df, outputfile)
  
  # Obtains distribution of numerical variables
  get_histograms(train_df, outputfile)
  
  # Obtains correlation map
  get_correlation_map(train_df, outputfile)

def get_summary_table(train_df, outputfile):
  summary_table = train_df.describe() # get summary table
  
  axis = plt.subplot(frame_on=False) # remove frame
  axis.xaxis.set_visible(False)  # remove x axis
  axis.yaxis.set_visible(False)  # remove y axis

  table(axis, summary_table)

  plt.savefig(outputfile + '/summary_table.png') # issue with saving file
  
def get_target_distribution(train_df, outputfile):
  distribution = alt.Chart(train_df).mark_bar().encode(
    x=alt.X("count()", title="Count"),
    y=alt.Y("Age")
  )
  save(distribution, outputfile + '/target_distribution.png')

def get_histograms(train_df, outputfile):
  histogram = alt.Chart(train_df).mark_bar(
    opacity=0.4
  ).encode(
    x=alt.X(alt.repeat(), type="quantitative", bin=alt.Bin(maxbins=50)),
    y=alt.Y("count()", stack=None)
  ).repeat(
    [
      "Length",
      "Diameter",
      "Height",
      "Whole weight",
      "Shucked weight",
      "Viscera weight",
      "Shell weight",
    ],
    columns=2
  )
  save(histogram, outputfile + '/histograms.png')

def get_correlation_map(train_df, outputfile):
  corr_df = (
    train_df.drop(["Sex", "Age"], axis=1)
    .corr("spearman")
    .abs()
    .stack()
    .reset_index(name="corr")
  )
  correlation = alt.Chart(corr_df).mark_rect().encode(
    x=alt.X("level_0", title=None),
    y=alt.Y("level_1", title=None),
    color=alt.Color("corr")
  ).properties(height=300, width=300)
  
  correlation_map = correlation + correlation.mark_text().encode(
    text=alt.Text("corr", format=',.2r'),
    color=alt.value('black')
    )
  save(correlation_map, outputfile + '/correlation_map.png')

#if __name__ == "__main__":
  #main(opt[--train_path], opt[--output_file])
  
df = pd.read_csv('../../data/raw/abalone.data')
train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)