from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models import InferenceRequest
from app.services.data_operations import inference_model

router = APIRouter()

@router.post("/inference-model/")
async def inference(request: InferenceRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(inference_model, request)
        return {"message": f"Inference started for model {request.model_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
