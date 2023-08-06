import pandas as pd
from config.core import config
from processing.data_manager import load_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, plot_roc_curve, roc_auc_score)
from sklearn.model_selection import (GridSearchCV, cross_val_score,
                                     train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from my_model.train_pipeline import run_training
from my_model.pipeline import genero_pipe




