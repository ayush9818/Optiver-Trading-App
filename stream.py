import boto3
import json

def send_data_to_kinesis(stream_name, data, partition_key):
    kinesis_client = boto3.client('kinesis')
    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),  # Assuming data is a dictionary that can be serialized to JSON
            PartitionKey=str(partition_key)  # A key used to distribute records across shards
        )
        print('Record sent to Kinesis:', response)
    except Exception as e:
        print('Error sending record to Kinesis:', e)

# Example usage
stream_name = 'optiver-stream'

stream_data = [{
    "data" : [{
            "stock_id": 0,
            "date_id": 400,
            "seconds_in_bucket": 0,
            "imbalance_size": 13964576.49,
            "imbalance_buy_sell_flag": 1,
            "reference_price": 0.999454,
            "matched_size": 10020705.2,
            "far_price": None,
            "near_price": None,
            "bid_price": 0.999648,
            "bid_size": 10312.0,
            "ask_price": 1.000521,
            "ask_size": 15275.08,
            "wap": 1.0,
            "target": 0.0500679,
            "time_id": 22000,
            "row_id": "400_0_0",
            "train_type": "test1"
        },
        {
            "stock_id": 1,
            "date_id": 400,
            "seconds_in_bucket": 0,
            "imbalance_size": 2003321.99,
            "imbalance_buy_sell_flag": 1,
            "reference_price": 0.998651,
            "matched_size": 1539364.28,
            "far_price": None,
            "near_price": None,
            "bid_price": 0.998065,
            "bid_size": 25527.0,
            "ask_price": 1.00258,
            "ask_size": 34190.0,
            "wap": 1.0,
            "target": -10.010004,
            "time_id": 22000,
            "row_id": "400_0_1",
            "train_type": "test1"
        },
        {
            "stock_id": 2,
            "date_id": 400,
            "seconds_in_bucket": 0,
            "imbalance_size": 1918830.43,
            "imbalance_buy_sell_flag": -1,
            "reference_price": 1.00047,
            "matched_size": 5088261.76,
            "far_price": None,
            "near_price": None,
            "bid_price": 0.999974,
            "bid_size": 3771.45,
            "ask_price": 1.001236,
            "ask_size": 179925.3,
            "wap": 1.0,
            "target": 7.070303,
            "time_id": 22000,
            "row_id": "400_0_2",
            "train_type": "test1"
        }],
    "commit" : True
}] 

while True:
    for d in stream_data:
        send_data_to_kinesis(stream_name, d, 1)

# for index in range(10):
#     data = {
#         'partition_key': 1,
#         'message': f'Hello, this is a test message {index}!'
#     }
#     send_data_to_kinesis(stream_name, data)
