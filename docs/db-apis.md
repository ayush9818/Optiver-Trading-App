# API Documentation

## Overview

This API provides endpoints for managing stock data, date mappings, model inferences, and models. The endpoints support operations such as retrieving data, creating new records, and ingesting data in batches.


## Endpoints

### Date Mappings

#### GET `/date_mappings/`

Retrieve a paginated list of date mappings based on the provided query parameters.

**Query Parameters:**
- `date_id` (Optional[int]): Filter by Date ID.
- `date` (Optional[dtdate]): Filter by Date.
- `page` (int, default=1): Page number.
- `page_size` (int, default=10): Number of results per page.

**Response:**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[DateMappingRequest]): List of date mapping requests.

**Example:**
```json
{
    "total_results": 100,
    "total_pages": 10,
    "page": 1,
    "page_size": 10,
    "data": [
        {
            "date_id": 1,
            "date": "2024-01-01"
        },
        ...
    ]
}
```

---

### Model Inferences

#### POST `/model-inferences/`

Create a new model inference record in the database.

**Request Body:**
- `model_id` (int): Unique identifier for the model.
- `date_id` (int): Identifier for the date.
- `predictions` (str): Predictions made by the model.

**Response:**
- `model_id` (int): Unique identifier for the model.
- `date_id` (int): Identifier for the date.
- `predictions` (str): Predictions made by the model.

**Example:**
```json
{
    "model_id": 1,
    "date_id": 1,
    "predictions": "Sample prediction"
}
```

#### GET `/model-inferences/`

Retrieve a paginated list of model inferences based on optional filtering criteria.

**Query Parameters:**
- `model_id` (Optional[int]): Filter by model ID.
- `date_id` (Optional[int]): Filter by date ID.
- `page` (int, default=1): Page number.
- `page_size` (int, default=10): Number of results per page.

**Response:**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[ModelInferenceRead]): List of model inference reads.

**Example:**
```json
{
    "total_results": 100,
    "total_pages": 10,
    "page": 1,
    "page_size": 10,
    "data": [
        {
            "id": 1,
            "model_id": 1,
            "date_id": 1,
            "predictions": "Sample prediction"
        },
        ...
    ]
}
```

---

### Models

#### POST `/models/`

Create a new model record in the database.

**Request Body:**
- `model_name` (str): Name of the model.
- `model_artifact_path` (str): Path to the model artifact.
- `date_id` (int): Identifier for the date.

**Response:**
- `message` (str): A message indicating the model was created successfully.

**Example:**
```json
{
    "message": "Model Created successfully."
}
```

#### GET `/models/`

Retrieve a paginated list of models based on optional filtering criteria.

**Query Parameters:**
- `model_id` (Optional[int]): Filter by model ID.
- `model_name` (Optional[str]): Filter by model name.
- `page` (int, default=1): Page number.
- `page_size` (int, default=10): Number of results per page.

**Response:**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[ModelDisplay]): List of model displays.

**Example:**
```json
{
    "total_results": 100,
    "total_pages": 10,
    "page": 1,
    "page_size": 10,
    "data": [
        {
            "model_id": 1,
            "model_name": "Sample Model",
            "model_artifact_path": "/path/to/artifact",
            "date_id": 1
        },
        ...
    ]
}
```

---

### Stock Data

#### GET `/stock_data/`

Retrieve a paginated list of stock data based on the provided query parameters.

**Query Parameters:**
- `start_date_id` (Optional[int]): Start of the date ID range.
- `end_date_id` (Optional[int]): End of the date ID range.
- `date_id` (Optional[int]): Specific date ID.
- `page` (int, default=1): Page number.
- `page_size` (int, default=10): Number of results per page.

**Response:**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[StockDataRequest]): List of stock data requests.

**Example:**
```json
{
    "total_results": 100,
    "total_pages": 10,
    "page": 1,
    "page_size": 10,
    "data": [
        {
            "stock_id": 1,
            "date_id": 1,
            "seconds_in_bucket": 60,
            "imbalance_size": 100.0,
            "imbalance_buy_sell_flag": 1,
            "reference_price": 150.0,
            "matched_size": 1000.0,
            "far_price": 155.0,
            "near_price": 145.0,
            "bid_price": 150.0,
            "bid_size": 200.0,
            "ask_price": 151.0,
            "ask_size": 250.0,
            "wap": 150.5,
            "target": 151.0,
            "time_id": 1,
            "row_id": "row_1",
            "train_type": "type_1"
        },
        ...
    ]
}
```

#### POST `/stock_data/`

Ingest new stock data records into the database.

**Request Body:**
- `commit` (bool): Flag to indicate if data should be committed to the database.
- `data` (List[StockDataRequest]): List of stock data requests to ingest.

**Response:**
- `message` (str): A message indicating the data was ingested successfully.

**Example:**
```json
{
    "message": "Data ingested successfully."
}
```

