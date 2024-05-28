import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from datetime import date, timedelta
import json
from typing import Dict, Any
import math
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)

# Load environment variables from .env file
load_dotenv()
env = os.environ


def get_secret():
    """
    Retrieve secret values from AWS Secrets Manager.

    Returns:
        dict: The secret values as a dictionary.

    Raises:
        ClientError: If there is an error retrieving the secret.
    """
    logger.info("Retrieving secret from AWS Secrets Manager.")
    # Create a Secrets Manager client
    session = boto3.session.Session(
        aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
        region_name=env.get("REGION_NAME"),
    )
    client = session.client(
        service_name="secretsmanager", region_name=env.get("REGION_NAME")
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=env.get("DB_SECRET")
        )
        logger.info("Secret retrieved successfully.")
    except ClientError as e:
        logger.error(f"Error retrieving secret: {e}")
        raise e

    # Parse the secret string into a dictionary
    secret = json.loads(get_secret_value_response["SecretString"])
    return secret


def get_date_from_date_id(date_id: int, total_data_ids: int) -> date:
    """
    Calculate the date corresponding to a given date_id.

    Args:
        date_id (int): The date ID.
        total_data_ids (int): The total number of date IDs.

    Returns:
        date: The calculated date.
    """
    logger.info(
        f"Calculating date for date_id: {date_id} with total_data_ids: {total_data_ids}."
    )
    today = date.today()
    days_to_subtract = total_data_ids - (date_id + 1)
    new_date = today - timedelta(days=days_to_subtract)
    logger.info(f"Calculated date: {new_date} for date_id: {date_id}.")
    return new_date


def apply_filters(query, model, filters: Dict[str, Any]):
    """
    Apply dynamic filters to a SQLAlchemy query based on model attributes and filter criteria.

    Args:
        query: The SQLAlchemy query object.
        model: The SQLAlchemy model class.
        filters (Dict[str, Any]): A dictionary of filters to apply.

    Returns:
        query: The modified SQLAlchemy query object.
    """
    logger.info("Applying filters to query.")
    for key, value in filters.items():
        if hasattr(model, key):
            attribute = getattr(model, key)
            if isinstance(
                value, list
            ):  # For handling list values in filters (e.g., date_id=[1,2,3])
                query = query.filter(attribute.in_(value))
            else:
                query = query.filter(attribute == value)
            logger.debug(f"Applied filter on {key} with value {value}.")
    return query


def clean_nan_values(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Replace all NaN float values with None.

    Args:
        item (Dict[str, Any]): The dictionary to clean.

    Returns:
        Dict[str, Any]: The cleaned dictionary.
    """
    logger.info("Cleaning NaN values from dictionary.")
    for key, value in item.items():
        if isinstance(value, float) and math.isnan(value):
            item[key] = None
            logger.debug(f"Replaced NaN in key {key} with None.")
    return item
