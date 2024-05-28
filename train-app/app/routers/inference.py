from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models import InferenceRequest
from app.services.data_operations import inference_model
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)

router = APIRouter()


@router.post("/inference-model/")
async def inference(request: InferenceRequest, background_tasks: BackgroundTasks):
    """
    Start an inference task for the specified model in the background.

    Args:
        request (InferenceRequest): The inference request data.
        background_tasks (BackgroundTasks): FastAPI background tasks dependency.

    Returns:
        dict: A message indicating that the inference task has started.

    Raises:
        HTTPException: If there is an error starting the inference task.
    """
    try:
        logger.info(f"Starting inference for model {request.model_id}.")
        # Add the inference task to be run in the background
        background_tasks.add_task(inference_model, request)
        logger.info(
            f"Inference task added to background tasks for model {request.model_id}."
        )
        return {"message": f"Inference started for model {request.model_id}"}
    except Exception as e:
        logger.error(f"Error starting inference for model {request.model_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
