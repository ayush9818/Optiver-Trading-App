from pydantic import BaseModel, Field
from datetime import date as dtdate
from typing import List, Optional, Any

# Pydantic models for data validation and API interaction

class StockDataRequest(BaseModel):
    """
    Request model for Stock Data.

    Attributes:
        stock_id (int): Unique identifier for the stock.
        date_id (int): Identifier for the date.
        seconds_in_bucket (int): Number of seconds in the bucket.
        imbalance_size (float): Size of the imbalance.
        imbalance_buy_sell_flag (int): Flag indicating buy or sell imbalance.
        reference_price (float): Reference price of the stock.
        matched_size (float): Size of matched orders.
        far_price (Any): Far price of the stock.
        near_price (Any): Near price of the stock.
        bid_price (Any): Bid price of the stock.
        bid_size (Any): Bid size of the stock.
        ask_price (Any): Ask price of the stock.
        ask_size (Any): Ask size of the stock.
        wap (float): Weighted average price.
        target (float): Target price.
        time_id (int): Time identifier.
        row_id (str): Row identifier.
        train_type (str): Type of training.
    """
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
    train_type: str

class DateMappingRequest(BaseModel):
    """
    Request model for Date Mapping.

    Attributes:
        date_id (int): Identifier for the date.
        date (dtdate): The actual date.
    """
    date_id: int
    date: dtdate

    class Config:
        orm_mode = True

class PageRequest(BaseModel):
    """
    Model for paginated responses of Stock Data.

    Attributes:
        total_results (int): Total number of results.
        total_pages (int): Total number of pages.
        page (int): Current page number.
        page_size (int): Number of results per page.
        data (List[StockDataRequest]): List of stock data requests.
    """
    total_results: int
    total_pages: int
    page: int
    page_size: int
    data: List[StockDataRequest]

class PageDateRequest(BaseModel):
    """
    Model for paginated responses of Date Mappings.

    Attributes:
        total_results (int): Total number of results.
        total_pages (int): Total number of pages.
        page (int): Current page number.
        page_size (int): Number of results per page.
        data (List[DateMappingRequest]): List of date mapping requests.
    """
    total_results: int
    total_pages: int
    page: int
    page_size: int
    data: List[DateMappingRequest]

class IngestRequest(BaseModel):
    """
    Request model for ingesting stock data.

    Attributes:
        commit (bool): Flag to indicate if data should be committed to the database.
        data (List[StockDataRequest]): List of stock data requests to ingest.
    """
    commit: bool
    data: List[StockDataRequest]

class DateMappingQueryParams(BaseModel):
    """
    Query parameters for filtering Date Mappings.

    Attributes:
        date_id (Optional[int]): Filter by Date ID.
        date (Optional[dtdate]): Filter by Date.
    """
    date_id: Optional[int] = Field(default=None, description="Filter by Date ID")
    date: Optional[dtdate] = Field(default=None, description="Filter by Date")

class StockDataQueryParams(BaseModel):
    """
    Query parameters for filtering Stock Data.

    Attributes:
        start_date_id (Optional[int]): Start of the date ID range.
        end_date_id (Optional[int]): End of the date ID range.
        date_id (Optional[int]): Specific date ID.
    """
    start_date_id: Optional[int] = Field(None, description="Start of the date ID range")
    end_date_id: Optional[int] = Field(None, description="End of the date ID range")
    date_id: Optional[int] = Field(None, description="Date ID")

class ModelCreate(BaseModel):
    """
    Request model for creating a Model.

    Attributes:
        model_name (str): Name of the model.
        model_artifact_path (str): Path to the model artifact.
        date_id (int): Identifier for the date.
    """
    model_name: str
    model_artifact_path: str
    date_id: int

class ModelDisplay(BaseModel):
    """
    Model for displaying a Model.

    Attributes:
        model_id (int): Unique identifier for the model.
        model_name (str): Name of the model.
        model_artifact_path (str): Path to the model artifact.
        date_id (int): Identifier for the date.
    """
    model_id: int
    model_name: str
    model_artifact_path: str
    date_id: int

    class Config:
        orm_mode = True

class PageModelRequest(BaseModel):
    """
    Model for paginated responses of Models.

    Attributes:
        total_results (int): Total number of results.
        total_pages (int): Total number of pages.
        page (int): Current page number.
        page_size (int): Number of results per page.
        data (List[ModelDisplay]): List of model displays.
    """
    total_results: int
    total_pages: int
    page: int
    page_size: int
    data: List[ModelDisplay]

class ModelInferenceBase(BaseModel):
    """
    Base model for Model Inference.

    Attributes:
        model_id (int): Unique identifier for the model.
        date_id (int): Identifier for the date.
        predictions (str): Predictions made by the model.
    """
    model_id: int
    date_id: int
    predictions: str

class ModelInferenceCreate(ModelInferenceBase):
    """
    Request model for creating Model Inference.
    """
    pass

class ModelInferenceRead(ModelInferenceBase):
    """
    Model for reading Model Inference.

    Attributes:
        id (int): Unique identifier for the inference.
    """
    id: int

    class Config:
        orm_mode = True

class PageModelInference(BaseModel):
    """
    Model for paginated responses of Model Inferences.

    Attributes:
        total_results (int): Total number of results.
        total_pages (int): Total number of pages.
        page (int): Current page number.
        page_size (int): Number of results per page.
        data (List[ModelInferenceRead]): List of model inference reads.
    """
    total_results: int
    total_pages: int
    page: int
    page_size: int
    data: List[ModelInferenceRead]
