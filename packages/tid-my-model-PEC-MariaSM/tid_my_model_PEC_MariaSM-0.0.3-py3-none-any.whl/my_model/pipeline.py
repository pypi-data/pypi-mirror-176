! pip install -U feature-engine

#TODOS LOS IMPORTS
# data manipulation and plotting

import pandas as pd
import numpy as np

#for saving the pipeline
import joblib

#from Scikit-learn
from sklearn.pipeline import Pipeline

#from feature-engine
from feature_engine.imputation import (
    MeanMedianImputer,
    AddMissingIndicator
)

from feature_engine.selection import DropFeatures

#to separate training and test
from sklearn.model_selection import train_test_split

#the model
from sklearn.linear_model import LogisticRegression

from my_model.config.core import config

# set up the pipeline
genero_pipe = Pipeline([
    
    #====IMPUTATION ====
    ('drop_features', DropFeatures(features_to_drop=config.model_config.drop_features)),
    # add missing indicator
    ('missing_indicator', AddMissingIndicator(variables=config.model_config.numerical_vars_with_na)),
    
    #impute numerical variables with the mean
    ('mean_imputation', MeanMedianImputer(
        imputation_method='mean', variables=config.model_config.numerical_vars_with_na
    )),
    ('LogisticRegression', LogisticRegression())
])