import requests
import json 
import os 
from api_handler import APIHandler


if __name__ == "__main__":
    base_url = "http://localhost:80"  # Replace with your actual API base URL
    api_handler = APIHandler(base_url, page_size=50)
    data_dir = '/home/ayush1/optiver_app/data/api_data'
    os.makedirs(data_dir, exist_ok=True)

    # query_params = {
    #     "start_date_id" : 20,
    #     "end_date_id" : 22
    # }

    query_params = {
        "date_id" : 50
    }

    result = api_handler.get(api_url = '/get_stock_data/', params=query_params)
    with open(os.path.join(data_dir,'get_stock_data_date_id.json'),'w') as f:
        json.dump(result, f)
    
