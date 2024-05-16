import requests
import json 
import os 
from api_handler import APIHandler

base_api = "http://127.0.0.1:8000"  
inference_api = "/model-inferences/"

params = {"model_id" : 10, "date_id" : 10}
api_handler = APIHandler(base_api)
print(api_handler.get(inference_api, params))

# data = {"model_id" : 10, "date_id" : 10, "predictions" : "test-path"}
# api_handler.post(inference_api, data)