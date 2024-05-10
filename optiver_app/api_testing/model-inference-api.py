import requests
import json 
import os 
from api_handler import APIHandler

base_api = "http://localhost:8000"  
inference_api = "/model-inferences/"

params = {"model_id" : 10, "date_id" : 10}
api_handler = APIHandler(base_api)
api_handler.get(inference_api, params)