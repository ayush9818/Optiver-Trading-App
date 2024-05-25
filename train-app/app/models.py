from pydantic import BaseModel, Field
from typing import Optional

class TrainRequest(BaseModel):
    """
    Model for a training request.

    Attributes:
        model_id (int): Initial model to be fine-tuned.
        model_name (str): New model name.
        start_date_id (Optional[int]): Start of the date ID range.
        end_date_id (Optional[int]): End of the date ID range.
        date_id (Optional[int]): Specific date ID.
    """
    model_id: int  # initial model to be fine-tuned
    model_name: str  # new model name
    start_date_id: Optional[int] = Field(None, description="Start of the date ID range")
    end_date_id: Optional[int] = Field(None, description="End of the date ID range")
    date_id: Optional[int] = Field(None, description="Date ID")

class InferenceRequest(BaseModel):
    """
    Model for an inference request.

    Attributes:
        model_id (int): ID of the model to use for inference.
        pred_date_id (int): Date ID for the prediction.
    """
    model_id: int
    pred_date_id: int
