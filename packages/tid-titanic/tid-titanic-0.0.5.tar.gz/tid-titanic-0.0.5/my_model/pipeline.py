# data manipulation and plotting
import pandas as pd
import numpy as np

# for saving the pipeline
import joblib

# from Scikit-learn
from sklearn.pipeline import Pipeline

# from feature-engine
from feature_engine.imputation import (
    MeanMedianImputer,
    AddMissingIndicator,
    CategoricalImputer
)

from feature_engine.selection import DropFeatures

from sklearn.preprocessing import OneHotEncoder

#to separate training and test
from sklearn.model_selection import train_test_split

#the model
from sklearn.linear_model import LogisticRegression

from my_model.config.core import config

# set up the pipeline
survived_pipe = Pipeline([

    # ===== IMPUTATION =====
    ('drop_features', DropFeatures(features_to_drop=config.model_config.drop_features)),

    # add missing indicator in numerical
    ('missing_indicator_num', AddMissingIndicator(variables=config.model_config.numerical_vars_with_na)),

    # impute numerical variables with the mean
    ('mean_imputation', MeanMedianImputer(imputation_method='mean', variables=config.model_config.numerical_vars_with_na)),

    # impute categorical  variables with frequent
    ('freq_imputation_cat', CategoricalImputer(imputation_method= "frequent", variables=config.model_config.categorical_vars_with_na)),

    #  imputer, one-hot encoder
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False)),

    ('lr',LogisticRegression())
])
