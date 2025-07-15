import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGION = 'us-west-2'  

# Initializing clients
cloudwatch = boto3.client('cloudwatch', region_name=REGION)
cloudtrail = boto3.client('cloudtrail', region_name=REGION)

#Creating a CloudWatch alarm for S3 bucket size
def create_s3_bucket_size_alarm(bucket_name, threshold_gb=10):
    logger.info(f"Creating CloudWatch alarm for S3 bucket size: {bucket_name}")
    response = cloudwatch.put_metric_alarm(
        AlarmName=f'S3-{bucket_name}-Size-Alarm',
        MetricName='BucketSizeBytes',
        Namespace='AWS/S3',
        Statistic='Average',
        Period=86400,  # 1 day
        EvaluationPeriods=1,
        Threshold=threshold_gb * 1024 ** 3,  # Convert GB to bytes
        ComparisonOperator='GreaterThanThreshold',
        Dimensions=[
            {'Name': 'BucketName', 'Value': bucket_name},
            {'Name': 'StorageType', 'Value': 'StandardStorage'}
        ],
        AlarmActions=[],  # We can add SNS topic ARN for notifications if needed
        ActionsEnabled=False  # Set to True to enable actions
    )
    logger.info(f"Alarm created: {response['ResponseMetadata']['HTTPStatusCode']}")

# Enabling CloudTrail for auditing
def enable_cloudtrail(trail_name, s3_bucket_name):
    logger.info(f"Enabling CloudTrail: {trail_name}")
    try:
        response = cloudtrail.create_trail(
            Name=trail_name,
            S3BucketName=s3_bucket_name,
            IsMultiRegionTrail=True
        )
        cloudtrail.start_logging(Name=trail_name)
        logger.info(f"CloudTrail {trail_name} enabled and logging started.")
    except cloudtrail.exceptions.TrailAlreadyExistsException:
        logger.warning(f"CloudTrail {trail_name} already exists.")

# Creating a CloudWatch alarm for Glue job failures
def create_glue_job_failure_alarm(job_name):
    logger.info(f"Creating CloudWatch alarm for Glue job failures: {job_name}")
    response = cloudwatch.put_metric_alarm(
        AlarmName=f'Glue-{job_name}-Failure-Alarm',
        MetricName='FailedJobs',
        Namespace='AWS/Glue',
        Statistic='Sum',
        Period=300,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        Dimensions=[{'Name': 'JobName', 'Value': job_name}],
        AlarmActions=[],
        ActionsEnabled=False
    )
    logger.info(f"Alarm created: {response['ResponseMetadata']['HTTPStatusCode']}")

# Creating a CloudWatch alarm for Athena query failures
def create_athena_query_failure_alarm(workgroup):
    logger.info(f"Creating CloudWatch alarm for Athena query failures: {workgroup}")
    response = cloudwatch.put_metric_alarm(
        AlarmName=f'Athena-{workgroup}-QueryFailure-Alarm',
        MetricName='QueryFailed',
        Namespace='AWS/Athena',
        Statistic='Sum',
        Period=300,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        Dimensions=[{'Name': 'WorkGroup', 'Value': workgroup}],
        AlarmActions=[],
        ActionsEnabled=False
    )
    logger.info(f"Alarm created: {response['ResponseMetadata']['HTTPStatusCode']}")

if __name__ == "__main__":
    # resource names are confidential 
    create_s3_bucket_size_alarm('your-raw-bucket-name')
    create_glue_job_failure_alarm('supplychain-etl-job')
    create_athena_query_failure_alarm('supplychain-analytics-wg')
    enable_cloudtrail('supplychain-trail', 'your-raw-bucket-name') 