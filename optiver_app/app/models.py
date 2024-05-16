from pydantic import BaseModel, Field
from datetime import date as dtdate
from typing import List, Optional, Any

# Pydantic models for data validation
class StockDataRequest(BaseModel):
    stock_id: int
    date_id: int
    seconds_in_bucket: int
    imbalance_size: float
    imbalance_buy_sell_flag: int
    reference_price: float
    matched_size: float
    far_price: Any
    near_price: Any
    bid_price: Any
    bid_size: Any
    ask_price: Any
    ask_size: Any
    wap: float
    target: float
    time_id: int
    row_id: str
    train_type : str 

class DateMappingRequest(BaseModel):
    date_id: int
    date: dtdate

    class Config:
        orm_mode = True

class PageRequest(BaseModel):
    total_results : int
    total_pages : int 
    page : int 
    page_size : int 
    data : List[StockDataRequest]

class PageDateRequest(BaseModel):
    total_results : int
    total_pages : int 
    page : int 
    page_size : int 
    data : List[DateMappingRequest]

class IngestRequest(BaseModel):
    commit: bool
    data: List[StockDataRequest]

class DateMappingQueryParams(BaseModel):
    date_id: Optional[int] = Field(default=None, description="Filter by Date ID")
    date: Optional[dtdate] = Field(default=None, description="Filter by Date")

class StockDataQueryParams(BaseModel):
    start_date_id: Optional[int] = Field(None, description="Start of the date ID range")
    end_date_id: Optional[int] = Field(None, description="End of the date ID range")
    date_id: Optional[int] = Field(None, description="Date ID")

# Pydantic models to interact with the API
class ModelCreate(BaseModel):
    model_name: str
    model_artifact_path: str
    date_id : int 

class ModelDisplay(BaseModel):
    model_id: int
    model_name: str
    model_artifact_path: str
    date_id : int 

    class Config:
        orm_mode = True

class PageModelRequest(BaseModel):
    total_results : int
    total_pages : int 
    page : int 
    page_size : int 
    data : List[ModelDisplay]

class ModelInferenceBase(BaseModel):
    model_id: int
    date_id: int
    predictions: str

class ModelInferenceCreate(ModelInferenceBase):
    pass

class ModelInferenceRead(ModelInferenceBase):
    id: int

    class Config:
        orm_mode = True

class PageModelInference(BaseModel):
    total_results : int
    total_pages : int 
    page : int 
    page_size : int 
    data : List[ModelInferenceRead]
