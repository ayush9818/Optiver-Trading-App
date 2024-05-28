from api_handler import APIHandler


model_create_data = {
    "model_name": "optiver-base-model",
    "model_artifact_path": "trained_models/optiver-base-model.pickle",
}

base_url = "http://127.0.0.1:8000"
api_handler = APIHandler(base_url=base_url)

# api_handler.post('/models/', model_create_data)

print(api_handler.get("/models/", {}))

print(api_handler.get("/models/4", {}))
