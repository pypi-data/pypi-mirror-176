# TODOS LOS IMPORTS
# data manipulation and plotting


# from feature-engine
from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
from feature_engine.selection import DropFeatures
from feature_engine.encoding import OneHotEncoder

# the model
from sklearn.linear_model import LinearRegression

# from Scikit-learn
from sklearn.pipeline import Pipeline

from my_model.config.core import config

genero_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        # One hot encoding
        (
            "one_hot_encoding",
            OneHotEncoder(variables=['sex', 'smoker'])
        ),
        ("LinearRegression", LinearRegression()),
    ]
)
