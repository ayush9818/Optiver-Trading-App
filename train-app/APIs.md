
# API Documentation

## Base URL
All endpoints are relative to the base URL: `http://your-api-domain`

---

## 1. Inference Model
### Endpoint
`POST /inference-model/`

### Description
Starts an inference process for the specified model in the background.

### Request Body
**InferenceRequest**
- `model_id` (int): ID of the model to use for inference.
- `pred_date_id` (int): Date ID for which predictions are to be made.

### Example Request
```json
{
  "model_id": 1,
  "pred_date_id": 20230516
}
```

### Example Response
```json
{
  "message": "Inference started for model 1"
}
```

### Error Responses
- `500 Internal Server Error`: If an error occurs while starting the inference process.

---

## 2. Train Model
### Endpoint
`POST /train-model/`

### Description
Starts a training process for a new model based on the specified parameters in the background.

### Request Body
**TrainRequest**
- `model_id` (int): ID of the initial model to be fine-tuned.
- `model_name` (str): Name for the new model.
- `start_date_id` (Optional, int): Start of the date ID range for training data.
- `end_date_id` (Optional, int): End of the date ID range for training data.
- `date_id` (Optional, int): Specific date ID for training data.

### Example Request
```json
{
  "model_id": 1,
  "model_name": "new_finetuned_model",
  "start_date_id": 20230501,
  "end_date_id": 20230515
}
```

### Example Response
```json
{
  "message": "Training started for model new_finetuned_model"
}
```

### Error Responses
- `500 Internal Server Error`: If an error occurs while starting the training process.

---

### Usage Notes
1. **Background Tasks**: Both endpoints utilize FastAPI's `BackgroundTasks` to start the requested processes without blocking the main thread. This is useful for long-running tasks.
2. **Error Handling**: Each endpoint includes error handling to catch and respond with appropriate HTTP status codes and messages in case of failures.
