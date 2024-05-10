import requests
import json
import logging

logger = logging.getLogger('optiver.'+__name__)

class APIHandler:
    def __init__(self, base_url, page_size=50):
        self.base_url = base_url
        self.page_size = page_size

    def get(self, api_url, params):
        params['page_size'] = self.page_size
        url = self.base_url + api_url
        logger.info(f"API URL : {url}")
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
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)
        if response.status_code == 200:
            logger.info("Success")
        else:
            logger.error(f"Failed to ingest data: {response.status_code} - {response.text}")
            raise Exception("Model Already Exists")