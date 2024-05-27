import json
import base64
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        print(f'Decoded payload: {data}')

        # Call the ingest API
        ingest_api_url = 'http://optiver-db-alb-1648699209.us-east-1.elb.amazonaws.com:80/stock_data/'
        headers = {'Content-Type': 'application/json'}
        
        response = http.request(
            'POST',
            ingest_api_url,
            body=json.dumps(data),
            headers=headers
        )

        if response.status == 200:
            print('Data ingested successfully.')
        else:
            print(f'Failed to ingest data: {response.data}')

    return {
        'statusCode': 200,
        'body': json.dumps('Process completed')
    }
