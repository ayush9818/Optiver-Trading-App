import os
import boto3
from botocore.exceptions import ClientError
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)


class S3Handler:
    """
    A class to handle S3 operations such as downloading and uploading files.

    Attributes:
        bucket_name (str): The name of the S3 bucket.
        s3_client (boto3.client): The Boto3 S3 client.
    """

    def __init__(self):
        """
        Initialize the S3Handler with AWS credentials and S3 bucket information.
        """
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
        """
        Download a file from S3 to the local directory.

        Args:
            s3_path (str): The S3 path of the file to download.
            local_dir (str): The local directory to save the downloaded file.

        Returns:
            str: The local path of the downloaded file if successful, None otherwise.
        """
        try:
            file_name = os.path.basename(s3_path)
            local_path = os.path.join(local_dir, file_name)
            self.s3_client.download_file(self.bucket_name, s3_path, local_path)
            logger.info(f"File downloaded from S3: {s3_path} to {local_path}")
            return local_path
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            return None

    def upload_file(self, local_path, s3_path):
        """
        Upload a file from the local directory to S3.

        Args:
            local_path (str): The local path of the file to upload.
            s3_path (str): The S3 path to upload the file to.

        Returns:
            None
        """
        try:
            self.s3_client.upload_file(local_path, self.bucket_name, s3_path)
            logger.info(f"File uploaded to S3: {s3_path}")
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
