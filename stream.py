import boto3
import json
import pandas as pd 
import argparse
from loguru import logger 


def send_data_to_kinesis(stream_name, data, partition_key):
    kinesis_client = boto3.client('kinesis')
    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),  # Assuming data is a dictionary that can be serialized to JSON
            PartitionKey=str(partition_key)  # A key used to distribute records across shards
        )
        logger.info('Record sent to Kinesis:', response)
    except Exception as e:
        logger.info('Error sending record to Kinesis:', e)

def create_batches(data, batch_size):
    data_len = data.shape[0]

    for ind in range(0, data_len, batch_size):
        start_index = ind 
        end_index = min(data_len, start_index + batch_size)

        batch = data.iloc[start_index : end_index]
        batch = batch.to_dict(orient='records')
        yield batch 

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream-name", type=str, default='optiver-stream', help='Name of Kinesis stream in the console')
    parser.add_argument("--data-tag", type=str, default='demo_27', help='Train type tag of the data to be ingested')
    parser.add_argument("--data-path", type=str, default='data/stream_data.json', help='path to streaming data')
    parser.add_argument("--batch-size", type=int, default=50, help='batch size of the streaming data')

    args = parser.parse_args()
    logger.info(f"Stream Name : {args.stream_name} -- Data Tag : {args.data_tag} -- Batch Size : {args.batch_size}")

    data = pd.read_json(args.data_path)
    data['train_type'] = [args.data_tag] * len(data)

    for idx, batch in enumerate(create_batches(data, batch_size=args.batch_size)):
        logger.info(f"Batch ID : {idx+1}")
        stream_data = {
            "data"  : batch, 
            "commit" : True 
        }

        send_data_to_kinesis(args.stream_name, stream_data, 1)

        if idx == 10:
            break


