from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
from feature_engine.selection import DropFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from my_model.config.core import config

titanic_pipeline = Pipeline(
    [
        # ===== IMPUTATION =====
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        # add missing indicator
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_vars_with_na),
        ),
        # impute numerical variables with the mean
        (
            "mean_imputation",
            MeanMedianImputer(
                imputation_method="mean",
                variables=config.model_config.numerical_vars_with_na,
            ),
        ),
        ("LinearRegression", LinearRegression()),
    ]
)
