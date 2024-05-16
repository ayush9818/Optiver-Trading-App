from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models import TrainRequest
from app.services.data_operations import train_model

router = APIRouter()

@router.post("/train-model/")
async def train(request: TrainRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(train_model, request)
        return {"message": f"Training started for model {request.model_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
