"""
AutoML Configuration Settings
"""

# Page Configuration
PAGE_TITLE = "ML Yantra"
PAGE_LAYOUT = "wide"

# Model Training Configuration
DEFAULT_TEST_SIZE = 0.2
RANDOM_STATE = 42

# Classification Models Configuration
CLASSIFICATION_MODELS = {
    "max_iter": 1000,
    "n_estimators": 100,
    "kernel": "rbf"
}

# Regression Models Configuration
REGRESSION_MODELS = {
    "n_estimators": 100,
    "kernel": "rbf",
    "verbosity": 0
}

# Data Processing
PREVIEW_ROWS = 10
MAX_PREVIEW_ROWS = 20

# File Upload
SUPPORTED_FILE_TYPES = ['csv']
MAX_FILE_SIZE_MB = 200

# Encoding
ENCODING_METHODS = {
    "LABEL": "Label Encoding",
    "ONEHOT": "One-Hot Encoding",
    "ORDINAL": "Ordinal Encoding"
}

# Fill Methods for Null Values
FILL_METHODS = ["Mean", "Median", "Mode", "Forward Fill", "Backward Fill", "Custom Value"]

# Data Types
CONVERTIBLE_TYPES = ["int64", "float64", "object", "bool", "datetime64[ns]"]

# Metrics
CLASSIFICATION_METRICS = ["Accuracy", "Precision", "Recall", "F1-Score"]
REGRESSION_METRICS = ["MSE", "RMSE", "MAE", "R² Score"]
