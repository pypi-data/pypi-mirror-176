# TODOS LOS IMPORTS
# data manipulation and plotting
import numpy as np
import pandas as pd
# from feature-engine
from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
from feature_engine.selection import DropFeatures
from my_model.config.core import config
# the model
from sklearn.linear_model import LogisticRegression
#to separate training and test
from sklearn.model_selection import train_test_split
# from Scikit-learn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

genero_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        
        # impute numerical variables with the mean
        (
            "mean_imputation",
            MeanMedianImputer(
                imputation_method="mean",
                variables=config.model_config.numerical_vars_with_na,
            ),
        ),
        ('LogReg', LogisticRegression()),
    ]
)
