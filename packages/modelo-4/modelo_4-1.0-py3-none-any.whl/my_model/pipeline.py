# TODOS LOS IMPORTS
# data manipulation and plotting


# from feature-engine
#from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
#from feature_engine.selection import DropFeatures
from sklearn.preprocessing import StandardScaler
# the model
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
#from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from feature_engine.selection import DropFeatures
# from Scikit-learn
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import f_classif
from my_model.config.core import config

genero_pipe = Pipeline(
    [
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        (
            "scaler",
            StandardScaler(),
        ),
        (
            'random_forest', 
            RandomForestClassifier(criterion='gini',max_depth=8, n_estimators=200)),
    ]
)

