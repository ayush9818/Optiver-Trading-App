import warnings

warnings.filterwarnings("ignore")  # Ignore all warnings for clean output

import boto3
import json
import pandas as pd
import argparse
from loguru import logger


def send_data_to_kinesis(stream_name, data, partition_key):
    """
    Send data to an AWS Kinesis stream.

    Args:
        stream_name (str): The name of the Kinesis stream.
        data (dict): The data to send to the stream, should be serializable to JSON.
        partition_key (str): A key used to distribute records across shards.
    """
    kinesis_client = boto3.client("kinesis")
    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),  # Convert dictionary to JSON string
            PartitionKey=str(partition_key),  # Ensure the partition key is a string
        )
        logger.info("Record sent to Kinesis:", response)
    except Exception as e:
        logger.error("Error sending record to Kinesis:", e)


def create_batches(data, batch_size):
    """
    Create batches of data from a pandas DataFrame.

    Args:
        data (pd.DataFrame): The input data to be batched.
        batch_size (int): The size of each batch.

    Yields:
        list: A batch of data as a list of dictionaries.
    """
    data_len = data.shape[0]

    for ind in range(0, data_len, batch_size):
        start_index = ind
        end_index = min(data_len, start_index + batch_size)

        batch = data.iloc[start_index:end_index]
        # Drop 'id' column from each batch
        batch.drop(columns=["id"], axis=1, inplace=True)
        # Convert 'row_id' to string
        batch["row_id"] = batch["row_id"].astype("str")
        # Convert DataFrame to list of dictionaries
        batch = batch.to_dict(orient="records")
        yield batch


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stream-name",
        type=str,
        default="optiver-stream",
        help="Name of Kinesis stream in the console",
    )
    parser.add_argument(
        "--data-tag",
        type=str,
        default="demo_27",
        help="Train type tag of the data to be ingested",
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default="data/stream_data.json",
        help="Path to streaming data",
    )
    parser.add_argument(
        "--batch-size", type=int, default=50, help="Batch size of the streaming data"
    )

    args = parser.parse_args()
    logger.info(
        f"Stream Name: {args.stream_name} -- Data Tag: {args.data_tag} -- Batch Size: {args.batch_size}"
    )

    # Load data from the specified JSON file
    data = pd.read_json(args.data_path)
    # Add a 'train_type' column with the specified tag
    data["train_type"] = [args.data_tag] * len(data)

    # Process and send data in batches
    for idx, batch in enumerate(create_batches(data, batch_size=args.batch_size)):
        logger.info(f"Batch ID: {idx+1}")
        stream_data = {
            "data": batch,
            "commit": True,  # Include a 'commit' flag in the data
        }

        send_data_to_kinesis(args.stream_name, stream_data, 1)
