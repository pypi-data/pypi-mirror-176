# %%
# Default libs
import pandas as pd
#from matplotlib import pyplot as plt
import numpy as np
import time
import platform # to check user's version of Python
from tqdm import tqdm

# Detrend & deseason
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import signal
from statsmodels.tsa.stattools import adfuller
from statsmodels.formula.api import ols

# ML models
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors # Needed to suggest the best parameters for DBSCAN
from kneed import KneeLocator # Needed to suggest the best parameters for DBSCAN
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from ThymeBoost import ThymeBoost as tb
import optuna # for OCSVM parameters
#import orion
from sklearn.metrics import accuracy_score
from sklearn import metrics
from scipy.fft import rfft, rfftfreq
# %%
# Checking if the hook between Teams and DevOps is working.