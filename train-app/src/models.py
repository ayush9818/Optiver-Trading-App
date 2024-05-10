from pydantic import BaseModel, Field
from datetime import date as dtdate
from typing import List, Optional, Any



class TrainRequest(BaseModel):
    model_id : int
    model_name : str 
    start_date_id: Optional[int] = Field(None, description="Start of the date ID range")
    end_date_id: Optional[int] = Field(None, description="End of the date ID range")
    date_id: Optional[int] = Field(None, description="Date ID")

class InferenceRequest(BaseModel):
    model_id : int 
    pred_date_id : int 

   