import logging
import warnings
import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from mlflow import MlflowClient

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


warnings.filterwarnings("ignore")
np.random.seed(40)

# Read the wine-quality csv file from the URL
csv_url = (
    "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
)
try:
    data = pd.read_csv(csv_url, sep=";")
except Exception as e:
    logger.exception(
        "Unable to download training & test CSV, check your internet connection. Error: %s", e
    )

# Split the data into training and test sets. (0.75, 0.25) split.
train, test = train_test_split(data)

# The predicted column is "quality" which is a scalar from [3, 9]
train_x = train.drop(["quality"], axis=1)
test_x = test.drop(["quality"], axis=1)
train_y = train[["quality"]]
test_y = test[["quality"]]

# Set default values if no alpha is provided
alpha = 0.5 if float(sys.argv[1]) is None else float(sys.argv[1])
# in_alpha = 0.5
# alpha = 0.5 if float(in_alpha) is None else float(in_alpha)

# Set default values if no l1_ratio is provided
l1_ratio = 0.5 if float(sys.argv[2]) is None else float(sys.argv[2])
# in_l1_ratio = 0.5
# l1_ratio = 0.5 if float(in_l1_ratio) is None else float(in_l1_ratio)

# Useful for multiple runs (only doing one run in this sample notebook)
with mlflow.start_run():
    # Execute ElasticNet
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    # Evaluate Metrics
    predicted_qualities = lr.predict(test_x)
    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    # Print out metrics
    print(f"Elasticnet model (alpha={alpha:f}, l1_ratio={l1_ratio:f}):")
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    # Infer model signature - This is for local server of MLFlow
    # predictions = lr.predict(train_x)
    # signature = infer_signature(train_x, predictions)

    # For remote server only(DagsHub)
    remote_server_uri = "https://dagshub.com/binayak.mahapatra05/MLFlow-Deep-Learning.mlflow"
    mlflow.set_tracking_uri(remote_server_uri)

    # Log parameter, metrics, and model to MLflow
    mlflow.log_param("alpha", alpha)
    mlflow.log_param("l1_ratio", l1_ratio)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)

    tracking_url_type_store = ''
    if tracking_url_type_store != 'file':
        # Register the Model
        # There are other ways to use Model Registry, which depends on use case
        mlflow.sklearn.log_model(
            lr, "model", registered_model_name="ElasticnetWineModel")

    else:
        mlflow.sklearn.log_model(lr, "model")
        # Below code is for local server
        # mlflow.sklearn.log_model(lr, "model", signature=signature)

    client = MlflowClient()
    client.transition_model_version_stage(
        name="ElasticnetWineModel", version=5, stage="Staging"
    )
