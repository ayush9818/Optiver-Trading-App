import requests
import json

data = {
    "data": [
        {
            "stock_id": 10,
            "date_id": 488,
            "seconds_in_bucket": 0,
            "imbalance_size": 0.5,
            "imbalance_buy_sell_flag": 1,
            "reference_price": 100.0,
            "matched_size": 200.0,
            "far_price": 110.0,
            "near_price": 90.0,
            "bid_price": 95.0,
            "bid_size": 150.0,
            "ask_price": 105.0,
            "ask_size": 250.0,
            "wap": 100.0,
            "target": 120.0,
            "time_id": 1,
            "train_type": "dev",  # prod -> actual
            "row_id": "483_0_10",
        }
    ],
    "commit": True,
}

url = "http://localhost:80/ingest/"

# Convert the dictionary to JSON format
json_data = json.dumps(data)

# Set the appropriate headers for your request
headers = {"Content-Type": "application/json"}

# Make a POST request to the API endpoint
response = requests.post(url, data=json_data, headers=headers)

# Check the response from the server
if response.status_code == 200:
    print("Data ingested successfully")
else:
    print(f"Failed to ingest data: {response.status_code} - {response.text}")
