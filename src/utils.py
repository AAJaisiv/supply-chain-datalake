# Requirements: boto3, botocore must be installed in your environment
import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_file_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name = file_name
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        logger.info(f"Uploaded {file_name} to s3://{bucket}/{object_name}")
    except ClientError as e:
        logger.error(e)
        return False
    return True

def list_s3_objects(bucket, prefix=''):
    """
    List objects in an S3 bucket under a given prefix
    :param bucket: S3 bucket name
    :param prefix: S3 prefix (folder path)
    :return: List of object keys
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except ClientError as e:
        logger.error(e)
        return [] 