from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models import TrainRequest
from app.services.data_operations import train_model
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)

router = APIRouter()


@router.post("/train-model/")
async def train(request: TrainRequest, background_tasks: BackgroundTasks):
    """
    Start a model training task in the background.

    Args:
        request (TrainRequest): The training request data.
        background_tasks (BackgroundTasks): FastAPI background tasks dependency.

    Returns:
        dict: A message indicating that the training task has started.

    Raises:
        HTTPException: If there is an error starting the training task.
    """
    try:
        logger.info(f"Starting training for model {request.model_name}.")
        # Add the training task to be run in the background
        background_tasks.add_task(train_model, request)
        logger.info(
            f"Training task added to background tasks for model {request.model_name}."
        )
        return {"message": f"Training started for model {request.model_name}"}
    except Exception as e:
        logger.error(f"Error starting training for model {request.model_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
