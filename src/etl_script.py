# Requirements: This script is for AWS Glue (PySpark) and requires the AWS Glue and PySpark runtime.
# It will not run locally unless you have the AWS Glue libraries and Spark environment.
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get job arguments
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'input_path',
    'output_path'
])

input_path = args['s3://your-raw-bucket/input/test_data.csv'] 
output_path = args['s3://your-processed-bucket/output/processed_test_data/'] 
logger.info(f"Starting Glue ETL job: {args['JOB_NAME']}")
logger.info(f"Reading data from: {input_path}")
logger.info(f"Will write processed data to: {output_path}")

# Initialize Glue and Spark contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read raw CSV data from S3 as a DynamicFrame
dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_path]},
    format="csv",
    format_options={"withHeader": True}
)
logger.info(f"Read {dyf.count()} records from raw data.")

# Basic cleaning: drop nulls, cast types
dyf_clean = dyf.drop_nulls()
logger.info(f"After dropping nulls: {dyf_clean.count()} records remain.")

# Convert to DataFrame for advanced transformations
df = dyf_clean.toDF()
# Example: lower-case all column names
df = df.toDF(*[c.lower() for c in df.columns])


# Convert back to DynamicFrame for Glue output
dyf_out = DynamicFrame.fromDF(df, glueContext, "dyf_out")

# Write processed data as Parquet to S3
glueContext.write_dynamic_frame.from_options(
    frame=dyf_out,
    connection_type="s3",
    connection_options={"path": output_path},
    format="parquet"
)
logger.info(f"Wrote processed data to {output_path} in Parquet format.")

job.commit()
logger.info("Glue ETL job completed successfully.") 