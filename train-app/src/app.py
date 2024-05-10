from data_operations import (
    get_model, 
    fetch_train_data, 
    incremental_training, 
    ingest_model,
    run_inference

)
from time import time
import logging
import logging.config
from fastapi import FastAPI, BackgroundTasks, HTTPException
from models import TrainRequest, InferenceRequest
from pathlib import Path
import os 
import shutil 

logging.config.fileConfig('configs/logging/local.ini', disable_existing_loggers=False)
logger = logging.getLogger('optiver.'+__name__)

app = FastAPI()

async def train_model(request : TrainRequest):
    artifact_dir = Path(os.getcwd()) / f'artifacts/{int(time())}'
    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Setting Artifact Directory to artifact dir")

    base_model_path = get_model(model_id = request.model_id, artifact_dir = artifact_dir)
    logger.info("Base Model Path %s",base_model_path)

    train_data_path = fetch_train_data(request, artifact_dir)
    logger.info("Train Data Path %s", train_data_path)

    uploaded_path = incremental_training(train_data_path, base_model_path, artifact_dir, request.model_name)
    logger.info("Model Uploaded to %s", uploaded_path)

    ingest_model(model_name=request.model_name, model_artifact_path=uploaded_path)
    logger.info("Model Ingest Successfully")

    logger.info(f"Congratulations!! Training completed for model {request.model_name}")

    # Clean Up
    try:
        shutil.rmtree(artifact_dir)
    except:
        pass

async def inference_model(request : InferenceRequest):
    artifact_dir = Path(os.getcwd()) / f'artifacts/{int(time())}'
    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Setting Artifact Directory to artifact dir")

    model_path = get_model(model_id = request.model_id, artifact_dir = artifact_dir)
    logger.info("Model Path %s",model_path)

    inference_data_path = fetch_inference_data(request, artifact_dir)
    logger.info("Inference Data Path %s", inference_data_path)

    predictions_path = run_inference(model_path, inference_data_path, artifact_dir)
    logger.info("Predictions Uploaded to %s",predictions_path)

    



@app.get("/healthcheck/")
def hello():
    return {"message" : "healthy"}

@app.post("/train-model/")
async def train(request: TrainRequest, background_tasks: BackgroundTasks):
    try: 
        background_tasks.add_task(train_model, request)
        return {"message": f"Training started for model {request.model_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/inference-model/")
async def inference(request : InferenceRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(train_model, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
