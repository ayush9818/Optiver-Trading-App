import requests
import json
import os
from api_handler import APIHandler
from datetime import date, timedelta


if __name__ == "__main__":
    # base_url = "http://127.0.0.1:8000"  # Replace with your actual API base URL
    base_url = "http://localhost:80"
    api_handler = APIHandler(base_url, page_size=50)
    data_dir = "/home/ayush1/optiver_app/data/api_data"
    os.makedirs(data_dir, exist_ok=True)

    query_params = {"date_id": 50}

    result = api_handler.get(api_url="/date_mappings/", params=query_params)
    print(result)

    query_params = {"date": date.today() - timedelta(10)}

    result = api_handler.get(api_url="/date_mappings/", params=query_params)
    print(result)
