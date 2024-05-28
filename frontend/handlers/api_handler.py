import requests
import json


class APIHandler:
    def __init__(self, base_url, page_size=50):
        self.base_url = base_url
        self.page_size = page_size

    def get(self, api_url, params):
        params["page_size"] = self.page_size
        url = self.base_url + api_url
        print(f"API URL : {url}")
        all_data = []
        page = 1
        while True:
            params["page"] = page
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for any HTTP error status codes
            data = response.json()
            all_data.extend(data["data"])
            if page >= data["total_pages"]:
                break
            page += 1
        return all_data

    def post(self, api_url, data):
        url = self.base_url + api_url
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
            import pdb

            pdb.set_trace()
            print(f"Failed to ingest data: {response.status_code} - {response.text}")
