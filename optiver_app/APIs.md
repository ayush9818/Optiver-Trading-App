
# API Documentation

## Base URL
All endpoints are relative to the base URL: `http://your-api-domain`

---

## 1. Get Date Mappings
### Endpoint
`GET /date_mappings/`

### Description
Fetches date mappings based on the provided query parameters.

### Query Parameters
- `date_id` (Optional, int): Filter by Date ID.
- `date` (Optional, date): Filter by Date.
- `page` (Optional, int): Page number (default: 1).
- `page_size` (Optional, int): Number of results per page (default: 10).

### Response Model
**PageDateRequest**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[DateMappingRequest]): List of date mappings.

### Example Request
```
GET /date_mappings/?page=1&page_size=10
```

### Example Response
```json
{
  "total_results": 100,
  "total_pages": 10,
  "page": 1,
  "page_size": 10,
  "data": [
    {
      "date_id": 1,
      "date": "2024-05-16"
    },
    ...
  ]
}
```

---

## 2. Ingest Data
### Endpoint
`POST /stock_data/`

### Description
Ingests stock data into the database.

### Request Body
**IngestRequest**
- `commit` (bool): Whether to commit the transaction.
- `data` (List[StockDataRequest]): List of stock data to be ingested.

### Example Request
```json
{
  "commit": true,
  "data": [
    {
      "stock_id": 1,
      "date_id": 1,
      "seconds_in_bucket": 3600,
      "imbalance_size": 1000.0,
      "imbalance_buy_sell_flag": 1,
      "reference_price": 100.0,
      "matched_size": 500.0,
      "far_price": null,
      "near_price": null,
      "bid_price": null,
      "bid_size": null,
      "ask_price": null,
      "ask_size": null,
      "wap": 99.5,
      "target": 101.0,
      "time_id": 1,
      "row_id": "row1",
      "train_type": "train"
    }
  ]
}
```

### Example Response
```json
{
  "message": "Data ingested successfully."
}
```

---

## 3. Create Model Inference
### Endpoint
`POST /model-inferences/`

### Description
Creates a new model inference record.

### Request Body
**ModelInferenceCreate**
- `model_id` (int): ID of the model.
- `date_id` (int): ID of the date.
- `predictions` (str): Predictions made by the model.

### Response Model
**ModelInferenceRead**
- `id` (int): ID of the inference.
- `model_id` (int): ID of the model.
- `date_id` (int): ID of the date.
- `predictions` (str): Predictions made by the model.

### Example Request
```json
{
  "model_id": 1,
  "date_id": 1,
  "predictions": "prediction string"
}
```

### Example Response
```json
{
  "id": 1,
  "model_id": 1,
  "date_id": 1,
  "predictions": "prediction string"
}
```

---

## 4. Get Model Inferences
### Endpoint
`GET /model-inferences/`

### Description
Fetches model inferences based on `model_id` and `date_id`.

### Query Parameters
- `model_id` (int): ID of the model.
- `date_id` (int): ID of the date.
- `page` (Optional, int): Page number (default: 1).
- `page_size` (Optional, int): Number of results per page (default: 10).

### Response Model
**PageModelInference**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[ModelInferenceRead]): List of model inferences.

### Example Request
```
GET /model-inferences/?model_id=1&date_id=1&page=1&page_size=10
```

### Example Response
```json
{
  "total_results": 20,
  "total_pages": 2,
  "page": 1,
  "page_size": 10,
  "data": [
    {
      "id": 1,
      "model_id": 1,
      "date_id": 1,
      "predictions": "prediction string"
    },
    ...
  ]
}
```

---

## 5. Create Model
### Endpoint
`POST /models/`

### Description
Creates a new model.

### Request Body
**ModelCreate**
- `model_name` (str): Name of the model.
- `model_artifact_path` (str): Path to the model artifact.

### Example Request
```json
{
  "model_name": "example_model",
  "model_artifact_path": "/path/to/artifact"
}
```

### Example Response
```json
{
  "message": "Model Created successfully."
}
```

---

## 6. Get Models
### Endpoint
`GET /models/`

### Description
Fetches models based on `model_id` or `model_name`.

### Query Parameters
- `model_id` (Optional, int): ID of the model.
- `model_name` (Optional, str): Name of the model.
- `page` (Optional, int): Page number (default: 1).
- `page_size` (Optional, int): Number of results per page (default: 10).

### Response Model
**PageModelRequest**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[ModelDisplay]): List of models.

### Example Request
```
GET /models/?page=1&page_size=10
```

### Example Response
```json
{
  "total_results": 50,
  "total_pages": 5,
  "page": 1,
  "page_size": 10,
  "data": [
    {
      "model_id": 1,
      "model_name": "example_model",
      "model_artifact_path": "/path/to/artifact"
    },
    ...
  ]
}
```

---

## 7. Get Stock Data
### Endpoint
`GET /stock_data/`

### Description
Fetches stock data based on date ID or date range.

### Query Parameters
- `start_date_id` (Optional, int): Start of the date ID range.
- `end_date_id` (Optional, int): End of the date ID range.
- `date_id` (Optional, int): Date ID.
- `page` (Optional, int): Page number (default: 1).
- `page_size` (Optional, int): Number of results per page (default: 10).

### Response Model
**PageRequest**
- `total_results` (int): Total number of results.
- `total_pages` (int): Total number of pages.
- `page` (int): Current page number.
- `page_size` (int): Number of results per page.
- `data` (List[StockDataRequest]): List of stock data.

### Example Request
```
GET /get_stock_data/?start_date_id=1&end_date_id=10&page=1&page_size=10
```

### Example Response
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
      "seconds_in_bucket": 3600,
      "imbalance_size": 1000.0,
      "imbalance_buy_sell_flag": 1,
      "reference_price": 100.0,
      "matched_size": 500.0,
      "far_price": null,
      "near_price": null,
      "bid_price": null,
      "bid_size": null,
      "ask_price": null,
      "ask_size": null,
      "wap": 99.5,
      "target": 101.0,
      "time_id": 1,
      "row_id": "row1",
      "train_type": "train"
    },
    ...
  ]
}
```
