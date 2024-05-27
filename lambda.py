import json
import base64
import urllib3
import os

# Initialize the PoolManager for making HTTP requests
http = urllib3.PoolManager()

def lambda_handler(event, context):
    """
    AWS Lambda handler function to process Kinesis stream records and send them to an ingest API.

    Args:
        event (dict): The event data containing records from the Kinesis stream.
        context (object): The context in which the Lambda function is called.

    Returns:
        dict: A response dictionary with status code and message.
    """
    for record in event['Records']:
        # Decode the base64 encoded Kinesis data
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        print(f'Decoded payload: {data}')

        # Get the ingest API URL from environment variables
        ingest_api_url = os.getenv('INGEST_API_URL')
        print(ingest_api_url)
        
        headers = {'Content-Type': 'application/json'}

        # Make a POST request to the ingest API
        response = http.request(
            'POST',
            ingest_api_url,
            body=json.dumps(data),
            headers=headers
        )

        # Print the status of the response
        print(f'Status: {response.status}')
        if response.status == 200:
            print('Data ingested successfully.')
        else:
            print(f'Failed to ingest data: {response.data}')

    # Return a success response
    return {
        'statusCode': 200,
        'body': json.dumps('Process completed')
    }
