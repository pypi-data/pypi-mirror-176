# TODOS LOS IMPORTS
# data manipulation and plotting


from feature_engine.encoding import OneHotEncoder

# from feature-engine
from feature_engine.imputation import MeanMedianImputer
from feature_engine.selection import DropFeatures

# the model
from sklearn.naive_bayes import GaussianNB

# from Scikit-learn
from sklearn.pipeline import Pipeline

from my_model.config.core import config

survived_pipe = Pipeline(
    [
        # ('mapper', DataFrameMapper([(d, LabelBinarizer()) for d in dummies])
        # ===== IMPUTATION =====
        # quitamos las columnas que no nos daban información
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        # ponemos la media de la edad en las filas que contienen NAN
        (
            "mean_missing_data",
            MeanMedianImputer(
                variables=config.model_config.numerical_vars_with_na,
                imputation_method="mean",
            ),
        ),
        # convertimos las columnas categoricas en variables binarias
        ("one_hot", OneHotEncoder(variables=config.model_config.onehot)),
        ("GaussianNB", GaussianNB()),
    ]
)
