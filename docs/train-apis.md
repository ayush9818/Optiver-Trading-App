# API Documentation

## Overview

This API provides endpoints for managing model training and inference tasks. The endpoints support starting training and inference tasks in the background using FastAPI's `BackgroundTasks`.

## Endpoints

### Train Model

#### POST `/train-model/`

Start a model training task in the background.

**Request Body:**
- `model_id` (int): Initial model to be fine-tuned.
- `model_name` (str): New model name.
- `start_date_id` (Optional[int]): Start of the date ID range.
- `end_date_id` (Optional[int]): End of the date ID range.
- `date_id` (Optional[int]): Specific date ID.

**Response:**
- `message` (str): A message indicating that the training task has started.

**Example Request:**
```json
{
    "model_id": 1,
    "model_name": "new_model",
    "start_date_id": 100,
    "end_date_id": 200,
    "date_id": 150
}
```

**Example Response:**
```json
{
    "message": "Training started for model new_model"
}
```

**Error Responses:**
- `500 Internal Server Error`: If there is an error starting the training task.

---

### Inference Model

#### POST `/inference-model/`

Start an inference task for the specified model in the background.

**Request Body:**
- `model_id` (int): ID of the model to use for inference.
- `pred_date_id` (int): Date ID for the prediction.

**Response:**
- `message` (str): A message indicating that the inference task has started.

**Example Request:**
```json
{
    "model_id": 1,
    "pred_date_id": 200
}
```

**Example Response:**
```json
{
    "message": "Inference started for model 1"
}
```

**Error Responses:**
- `500 Internal Server Error`: If there is an error starting the inference task.

---

## Models

### TrainRequest

```json
{
    "model_id": 1,
    "model_name": "new_model",
    "start_date_id": 100,
    "end_date_id": 200,
    "date_id": 150
}
```

- `model_id` (int): Initial model to be fine-tuned.
- `model_name` (str): New model name.
- `start_date_id` (Optional[int]): Start of the date ID range.
- `end_date_id` (Optional[int]): End of the date ID range.
- `date_id` (Optional[int]): Specific date ID.

### InferenceRequest

```json
{
    "model_id": 1,
    "pred_date_id": 200
}
```

- `model_id` (int): ID of the model to use for inference.
- `pred_date_id` (int): Date ID for the prediction.