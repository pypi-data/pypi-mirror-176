from sklearn.pipeline import Pipeline

# from feature-engine
from feature_engine.imputation import (
    MeanMedianImputer,
    AddMissingIndicator
)

from feature_engine.encoding import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from model.config.core import config

pipe = Pipeline([

    # ===== IMPUTATION =====
    
    ('categorical_encoder', OneHotEncoder(top_categories=1, variables=config.model_config.categorical_vars
    )),
    ('LogisticRegression', LogisticRegression())
   
   ])