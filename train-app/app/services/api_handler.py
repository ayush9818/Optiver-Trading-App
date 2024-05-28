import requests
import json
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)


class APIHandler:
    """
    A class to handle API requests for a given base URL with support for pagination.

    Attributes:
        base_url (str): The base URL for the API.
        page_size (int): The number of results per page for paginated requests.
    """

    def __init__(self, base_url, page_size=50):
        """
        Initialize the APIHandler with a base URL and an optional page size.

        Args:
            base_url (str): The base URL for the API.
            page_size (int): The number of results per page for paginated requests (default is 50).
        """
        self.base_url = base_url
        self.page_size = page_size

    def get(self, api_url, params):
        """
        Perform a GET request to the specified API endpoint with pagination support.

        Args:
            api_url (str): The API endpoint to send the GET request to.
            params (dict): Query parameters to include in the request.

        Returns:
            list: A list of all data retrieved from the paginated API endpoint.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        """
        params["page_size"] = self.page_size
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
        logger.info(f"Retrieved {len(all_data)} items from API.")
        return all_data

    def post(self, api_url, data):
        """
        Perform a POST request to the specified API endpoint.

        Args:
            api_url (str): The API endpoint to send the POST request to.
            data (dict): The data to include in the POST request.

        Returns:
            None

        Raises:
            Exception: If the request fails with a non-2xx status code.
        """
        url = self.base_url + api_url
        json_data = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json_data, headers=headers)
        if response.ok:
            logger.info("Success")
        else:
            logger.error(
                f"Failed to ingest data: {response.status_code} - {response.text}"
            )
            raise Exception("Failed to ingest data")
