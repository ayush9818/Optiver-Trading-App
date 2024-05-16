import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from datetime import date, timedelta
import json
from typing import Dict , Any
import math

load_dotenv()
env = os.environ

def get_secret():
    # Create a Secrets Manager client
    session = boto3.session.Session(
                aws_access_key_id=env.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=env.get('AWS_SECRET_ACCESS_KEY'),
                region_name=env.get('REGION_NAME')
        )
    client = session.client(
        service_name='secretsmanager',
        region_name=env.get('REGION_NAME')
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=env.get('DB_SECRET')
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    return secret


def get_date_from_date_id(date_id, total_data_ids):
    today = date.today()
    # date.now() - [481 - (date_id+1)
    # Number of days you want to subtract
    days_to_subtract = total_data_ids - (date_id+1)
    # Calculate the new date
    new_date = today - timedelta(days=days_to_subtract)
    return new_date


def apply_filters(query, model, filters: Dict[str, Any]):
    """
    Apply dynamic filters to a SQLAlchemy query based on model attributes and filter criteria.
    """
    for key, value in filters.items():
        if hasattr(model, key):
            attribute = getattr(model, key)
            if isinstance(value, list):  # for handling list values in filters (e.g., date_id=[1,2,3])
                query = query.filter(attribute.in_(value))
            else:
                query = query.filter(attribute == value)
    return query

def clean_nan_values(item: Dict[str, Any]) -> Dict[str, Any]:
    """Replace all NaN float values with None."""
    for key, value in item.items():
        if isinstance(value, float) and math.isnan(value):
            item[key] = None
    return item