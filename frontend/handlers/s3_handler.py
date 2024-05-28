import os
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger("optiver." + __name__)


class S3Handler:
    def __init__(self):
        self.bucket_name = os.environ["S3_BUCKET_NAME"]
        access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        region = os.environ["REGION"]
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
        )

    def download_file(self, s3_path, local_dir):
        try:
            file_name = os.path.basename(s3_path)
            local_path = os.path.join(local_dir, file_name)
            self.s3_client.download_file(self.bucket_name, s3_path, local_path)
            return local_path
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            return None

    def upload_file(self, local_path, s3_path):
        try:
            self.s3_client.upload_file(local_path, self.bucket_name, s3_path)
            logger.info(f"File uploaded to S3: {s3_path}")
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
