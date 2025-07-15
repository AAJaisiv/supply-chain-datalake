# AWS Supply Chain Data Lake

A modern, end-to-end data engineering project demonstrating how to build a scalable, secure, and cost-optimized data lake on AWS for supply chain analytics. This project leverages S3, Glue, Athena, Redshift Spectrum, and Lake Formation, with CI/CD and monitoring best practices.

---

##  Project Structure

```
aws-supplychain-datalake/
├── data/
│   ├── raw/                # Source datasets (e.g., test_data.csv, plus any generated fake data)
│   └── processed/          # Cleaned, transformed data
├── diagrams/
│   └── architecture.mmd    # Mermaid/PlantUML diagrams for architecture & workflows
├── iac/
│   └── datalake_stack.yaml # CloudFormation template for AWS resources
├── src/
│   ├── etl.py              # Python ETL pipeline (Boto3, Glue, S3)
│   ├── etl_script.py       # Glue ETL script (PySpark)
│   ├── analytics.sql       # Athena/Redshift Spectrum SQL queries
│   └── utils.py            # Shared helper functions
├── ci-cd/
│   └── pipeline.yaml       # Example CI/CD pipeline (GitHub Actions)
├── monitoring/
│   └── cloudwatch_setup.py # CloudWatch/CloudTrail setup scripts
├── requirements.txt        # Python dependencies
└── README.md               # This documentation
```

---

## 🏢 Business Problem Statement

Supply chain organizations face challenges in consolidating, analyzing, and deriving insights from large volumes of structured and unstructured data. This project demonstrates how to build a robust AWS data lake to enable advanced analytics and business intelligence for supply chain operations.

---

## 🏗️ Architecture Overview

- **S3**: Central storage for raw and processed data
- **Glue**: ETL, Data Catalog, and schema management
- **Athena/Redshift Spectrum**: Serverless analytics and reporting
- **Lake Formation**: Security and governance
- **CI/CD**: Automated deployment and code quality
- **Monitoring**: CloudWatch and CloudTrail for observability

See `diagrams/architecture.mmd` for a high-level workflow diagram.

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd aws-supplychain-datalake
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure AWS credentials (via environment variables or AWS CLI):
   ```bash
   aws configure
   ```

---

## 🚀 Usage

1. **Deploy Infrastructure**
   - Deploy the CloudFormation stack:
     ```bash
     aws cloudformation deploy \
       --template-file iac/datalake_stack.yaml \
       --stack-name supplychain-datalake-stack \
       --parameter-overrides RawDataBucketName=<raw-bucket> ProcessedDataBucketName=<processed-bucket> \
       --capabilities CAPABILITY_NAMED_IAM
     ```
2. **Upload ETL Script to S3**
   - Place `src/etl_script.py` in the correct S3 location for Glue Job.
3. **Run ETL Pipeline**
   - Use `src/etl.py` to upload data, trigger Glue Crawler and Job.
4. **Query Data**
   - Use Athena or Redshift Spectrum with queries in `src/analytics.sql`.
5. **Monitor & Audit**
   - Use `monitoring/cloudwatch_setup.py` to set up alarms and enable CloudTrail.

---

## 🧠 Data

- **Raw Data**:  supply chain data
- **Processed Data**: Cleaned and transformed, stored as Parquet in S3
- **Schema**: Managed by AWS Glue Data Catalog

---

## 🤩 Extensibility

- Add new ETL logic in `src/etl_script.py` (PySpark)
- Expand analytics with more SQL in `src/analytics.sql`
- Integrate additional AWS services (e.g., Redshift, QuickSight)
- Enhance CI/CD with more tests or deployment stages

---

## 🎯 Outputs

- S3 buckets with raw and processed data
- Glue Data Catalog with discovered schemas
- Athena/Redshift Spectrum queries and results
- CloudWatch alarms and CloudTrail logs
- CI/CD pipeline for automated deployment

---

## 📄 License

Released under the **MIT License**. See `LICENSE` for details.

---

## 📊 Diagrams & CI/CD

- See `diagrams/architecture.mmd` for architecture
- See `ci-cd/pipeline.yaml` for CI/CD workflow
- See `monitoring/cloudwatch_setup.py` for monitoring setup

---

## 💡 Open Sourced:

1. Clone the repo
2. Install dependencies
3. Deploy infrastructure
4. Upload ETL scripts
5. Run the pipeline
6. Query and analyze data
7. Monitor and optimize

---
