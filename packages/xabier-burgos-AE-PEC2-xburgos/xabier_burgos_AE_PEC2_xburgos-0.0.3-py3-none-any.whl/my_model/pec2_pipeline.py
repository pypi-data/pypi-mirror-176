from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline

from my_model.config.core import config

titanic_pipeline = Pipeline(
    [
        # ===== IMPUTATION =====
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
        ("DecisionTreeClassifier", DecisionTreeClassifier(
            criterion='gini', min_samples_leaf=1, min_samples_split=10, 
            max_features='sqrt', random_state=config.model_config.random_state)
        ),
    ]
)
