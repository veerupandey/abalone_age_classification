# author: Nick
# date: 2021-11-25

"""Fit a logistic regression based on input train data.
Usage: model_analysis.py [--train=<train>] [--result=<result>]
Options:
[--train=<train>]       Train data set file path.
[--result=<result>]     Folder to store results.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.compose import (
    ColumnTransformer,
    make_column_transformer
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    cross_validate,
    train_test_split,
)


from docopt import docopt
import traceback
import logging as logger
import sys





categorical_feature = ['Sex']
numerical_features = ['Length', 'Diameter', 'Height', 'Whole weight', 
'Shucked weight', 'Viscera weight', 'Shell weight']
target = 'Is old'
drop_feature = ['Rings']

preprocessor = make_column_transformer(
(StandardScaler(), numerical_features),
(OneHotEncoder(handle_unknown="ignore", sparse=False), categorical_feature),
("drop", drop_feature),
)