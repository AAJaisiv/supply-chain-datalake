# Requirements: boto3, botocore must be installed in your environment
import os
import logging
import boto3
from botocore.exceptions import ClientError
from utils import upload_file_to_s3, list_s3_objects

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration (can be set via environment variables or hardcoded for demo)
RAW_BUCKET = os.getenv('RAW_DATA_BUCKET', 'your-raw-bucket-name')
PROCESSED_BUCKET = os.getenv('PROCESSED_DATA_BUCKET', 'your-processed-bucket-name')
RAW_DATA_FILE = os.getenv('RAW_DATA_FILE', 'data/raw/test_data.csv')
S3_RAW_KEY = os.getenv('S3_RAW_KEY', 'input/test_data.csv')
GLUE_CRAWLER_NAME = os.getenv('GLUE_CRAWLER_NAME', 'raw-data-crawler')
GLUE_JOB_NAME = os.getenv('GLUE_JOB_NAME', 'supplychain-etl-job')

# Initialize AWS clients
s3_client = boto3.client('s3')
glue_client = boto3.client('glue')

def upload_raw_data():
    """
    Uploading raw data file to S3 bucket
    """
    logger.info(f"Uploading {RAW_DATA_FILE} to s3://{RAW_BUCKET}/{S3_RAW_KEY}")
    success = upload_file_to_s3(RAW_DATA_FILE, RAW_BUCKET, S3_RAW_KEY)
    if not success:
        logger.error("Failed to upload raw data to S3.")
        exit(1)
    logger.info("Raw data uploaded successfully.")

def trigger_glue_crawler():
    """
    Starting the Glue Crawler to update the Data Catalog
    """
    logger.info(f"Triggering Glue Crawler: {GLUE_CRAWLER_NAME}")
    try:
        response = glue_client.start_crawler(Name=GLUE_CRAWLER_NAME)
        logger.info("Glue Crawler started.")
    except ClientError as e:
        logger.error(f"Failed to start Glue Crawler: {e}")
        exit(1)

def trigger_glue_job():
    """
    Starting the Glue ETL Job for data transformation
    """
    logger.info(f"Triggering Glue Job: {GLUE_JOB_NAME}")
    try:
        response = glue_client.start_job_run(JobName=GLUE_JOB_NAME)
        job_run_id = response['JobRunId']
        logger.info(f"Glue Job started. JobRunId: {job_run_id}")
        return job_run_id
    except ClientError as e:
        logger.error(f"Failed to start Glue Job: {e}")
        exit(1)

def verify_processed_data():
    """
    List processed data files in the processed S3 bucket
    """
    logger.info(f"Listing processed data in s3://{PROCESSED_BUCKET}/output/")
    objects = list_s3_objects(PROCESSED_BUCKET, prefix='output/')
    if objects:
        logger.info(f"Processed data files: {objects}")
    else:
        logger.warning("No processed data files found.")

def main():
    upload_raw_data()
    trigger_glue_crawler()
    # Optionally, wait for crawler to finish before starting job
    trigger_glue_job()
    verify_processed_data()

if __name__ == "__main__":
    main() 