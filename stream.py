import boto3
import json

def send_data_to_kinesis(stream_name, data):
    kinesis_client = boto3.client('kinesis',
                            region_name='us-east-1',
                            aws_access_key_id='AKIAQ3EGPYOWBVYN6BQO',
                            aws_secret_access_key='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')
    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),  # Assuming data is a dictionary that can be serialized to JSON
            PartitionKey=str(data['partition_key'])  # A key used to distribute records across shards
        )
        print('Record sent to Kinesis:', response)
    except Exception as e:
        print('Error sending record to Kinesis:', e)

# Example usage
stream_name = 'optiver-data-stream'
data = {
    'partition_key': 1,
    'message': 'Hello, this is a test message!'
}
send_data_to_kinesis(stream_name, data)
