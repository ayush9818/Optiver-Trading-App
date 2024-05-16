import os
import logging
import logging.config
from time import time
from pathlib import Path
import shutil
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from app.services.api_handler import APIHandler
from app.services.s3_handler import S3Handler
from app.models import TrainRequest, InferenceRequest
from dotenv import load_dotenv

logging.config.fileConfig('app/configs/logging/local.ini', disable_existing_loggers=False)
logger = logging.getLogger('optiver.' + __name__)

load_dotenv()

def get_model(model_id, artifact_dir):
    base_url = os.getenv('BASE_API')
    model_api = os.getenv('MODEL_API')
    params = {
        'model_id' : model_id
    }

    api_handler = APIHandler(base_url=base_url)
    data = api_handler.get(model_api, params)[0]

    model_artifact_path = data['model_artifact_path']

    base_model_path = S3Handler().download_file(model_artifact_path, artifact_dir)
    return base_model_path

def fetch_train_data(data_params, artifact_dir):
    params = {
        'start_date_id': data_params.start_date_id,
        'end_date_id': data_params.end_date_id,
        'date_id': data_params.date_id
    }

    base_api = os.getenv('BASE_API')
    data_api = os.getenv('DATA_API')

    api_handler = APIHandler(base_api)
    data = api_handler.get(data_api, params)
    data = pd.DataFrame(data)
    data = data[data.train_type == 'prod']
    data.drop('train_type', axis=1, inplace=True)

    data.to_csv(artifact_dir / 'train_data.csv', index=False)
    return artifact_dir / 'train_data.csv'

def fetch_inference_data(data_params, artifact_dir):
    assert data_params.pred_date_id > 1
    logger.info(f"Prediction Date ID: {data_params.pred_date_id}")
    logger.info(f"Fetching Data for {data_params.pred_date_id - 1} DateID")

    params = {
        'start_date_id': None,
        'end_date_id': None,
        'date_id': data_params.pred_date_id - 1
    }

    base_api = os.getenv('BASE_API')
    data_api = os.getenv('DATA_API')

    api_handler = APIHandler(base_api)
    data = api_handler.get(data_api, params)
    data = pd.DataFrame(data)
    data = data[data.train_type == 'prod']
    data.drop('train_type', axis=1, inplace=True)

    data.to_csv(artifact_dir / 'inference_data.csv', index=False)
    return artifact_dir / 'inference_data.csv'

def generate_features(df):
    features = ['seconds_in_bucket', 'imbalance_buy_sell_flag', 'imbalance_size', 'matched_size',
                'bid_size', 'ask_size', 'reference_price', 'far_price', 'near_price', 'ask_price',
                'bid_price', 'wap', 'imb_s1', 'imb_s2']
    
    df = df.copy()
    
    df['imb_s1'] = (df['bid_size'] - df['ask_size']) / (df['bid_size'] + df['ask_size'])
    df['imb_s2'] = (df['imbalance_size'] - df['matched_size']) / (df['matched_size'] + df['imbalance_size'])
    
    prices = ['reference_price', 'far_price', 'near_price', 'ask_price', 'bid_price', 'wap']
    for i, a in enumerate(prices):
        for j, b in enumerate(prices[i+1:], i+1):
            df[f'{a}_{b}_diff'] = df[a] - df[b]
            features.append(f'{a}_{b}_diff')
    return df, features

def incremental_training(data_path, base_model_path, artifact_dir, model_name):
    df_train = pd.read_csv(data_path)

    initial_model = pickle.load(open(base_model_path, 'rb'))

    df_train = df_train.dropna(subset=['target']).copy()
    df_train, feature_names = generate_features(df_train)

    feature_names = df_train.drop(columns=['target', 'date_id', 'stock_id']).columns.tolist()
    X = df_train[feature_names].values
    y = df_train['target'].values

    xgboost_models = []
    xgboost_cv_errors = []
    tscv = TimeSeriesSplit(n_splits=5)
    
    for train_index, test_index in tscv.split(X):
        X_train_cv, X_test_cv = X[train_index], X[test_index]
        y_train_cv, y_test_cv = y[train_index], y[test_index]

        dtrain = xgb.DMatrix(X_train_cv, label=y_train_cv)
        dtest = xgb.DMatrix(X_test_cv, label=y_test_cv)
        params = {'objective': 'reg:squarederror', 'eval_metric': 'mae', 'learning_rate': 0.01}
        model_xgb = xgb.train(params, dtrain, num_boost_round=50, evals=[(dtest, 'eval')],
                              early_stopping_rounds=30, verbose_eval=False, xgb_model=initial_model)
        xgboost_models.append(model_xgb)
        xgboost_cv_errors.append(model_xgb.best_score)

    average_mae = np.mean(xgboost_cv_errors)
    logger.info(f"Average MAE across all folds: {average_mae}")

    model_filename = f'{model_name}.pickle'
    with open(artifact_dir / model_filename, 'wb') as f:
        pickle.dump(xgboost_models[-1], f)

    s3_path = f"trained_models/{model_filename}"
    s3_client = S3Handler()
    s3_client.upload_file(artifact_dir / model_filename, s3_path)
    return s3_path

def run_inference(model_path, data_path, artifact_dir, request: InferenceRequest):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    infer_df = pd.read_csv(data_path)
    infer_df = infer_df.dropna(subset=['target']).copy()
    infer_df, feature_names = generate_features(infer_df)

    feature_names = infer_df.drop(columns=['target', 'date_id', 'stock_id']).columns.tolist()

    X_inference = infer_df[feature_names].values

    d_inference = xgb.DMatrix(X_inference)
    predictions = model.predict(d_inference)

    infer_df['prediction'] = predictions

    inference_filename = f'inference_{request.model_id}_{request.pred_date_id}.csv'
    infer_df.to_csv(artifact_dir / inference_filename, index=False)

    s3_path = f"inference_data/{inference_filename}"
    s3_client = S3Handler()
    s3_client.upload_file(artifact_dir / inference_filename, s3_path)
    return s3_path

def ingest_model(model_name, date_id, model_artifact_path):
    try:
        base_api = os.getenv('BASE_API')
        model_api = os.getenv('MODEL_API')
        if not base_api or not model_api:
            raise EnvironmentError("API environment variables are not set properly.")

        api_handler = APIHandler(base_api)
        data = {
            "model_name": model_name,
            "model_artifact_path": model_artifact_path,
            "date_id" : date_id 
        }
        api_handler.post(model_api, data)
    except Exception as e:
        logger.error(f"Failed to ingest model: {e}")
        raise

def ingest_inference(date_id, model_id, prediction_path):
    try:
        base_api = os.getenv('BASE_API')
        inference_api = os.getenv('INFERENCE_API')
        if not base_api or not inference_api:
            raise EnvironmentError("API environment variables are not set properly.")

        api_handler = APIHandler(base_api)
        data = {
            "model_id": model_id,
            "date_id": date_id,
            "predictions": prediction_path
        }
        api_handler.post(inference_api, data)
    except Exception as e:
        logger.error(f"Failed to ingest inference data: {e}")
        raise

async def train_model(request: TrainRequest):
    artifact_dir = Path(os.getcwd()) / f'artifacts/{int(time())}'
    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Setting Artifact Directory to artifact dir")

    base_model_path = get_model(request.model_id, artifact_dir)
    logger.info("Base Model Path %s", base_model_path)

    train_data_path = fetch_train_data(request, artifact_dir)
    logger.info("Train Data Path %s", train_data_path)

    uploaded_path = incremental_training(train_data_path, base_model_path, artifact_dir, request.model_name)
    logger.info("Model Uploaded to %s", uploaded_path)

    ingest_model(request.model_name, request.date_id, uploaded_path)
    logger.info("Model Ingest Successfully")

    logger.info(f"Congratulations!! Training completed for model {request.model_name}")

    try:
        shutil.rmtree(artifact_dir)
    except Exception as e:
        logger.error("Error cleaning up artifacts: %s", str(e))

async def inference_model(request: InferenceRequest):
    artifact_dir = Path(os.getcwd()) / f'artifacts/{int(time())}'
    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Setting Artifact Directory to artifact dir")

    model_path = get_model(request.model_id, artifact_dir)
    logger.info("Model Path %s", model_path)

    inference_data_path = fetch_inference_data(request, artifact_dir)
    logger.info("Inference Data Path %s", inference_data_path)

    predictions_path = run_inference(model_path, inference_data_path, artifact_dir, request)
    logger.info("Predictions Uploaded to %s", predictions_path)

    ingest_inference(request.pred_date_id, request.model_id, predictions_path)
    logger.info("Inference Ingestion Success!!")

    try:
        shutil.rmtree(artifact_dir)
    except Exception as e:
        logger.error("Error cleaning up artifacts: %s", str(e))

