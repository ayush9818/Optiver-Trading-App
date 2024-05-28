from api_handler import APIHandler


base_api = "http://54.87.86.15:81"
train_api = "/train-model/"

data = {"model_id": 3, "model_name": "api-test-4", "date_id": 380}

api_handler = APIHandler(base_api)
api_handler.post(train_api, data)
