-- Athena/Redshift Spectrum Analytics SQL
-- Glue Database: supplychain_datalake
-- Table: processed_test_data (assumed name; adjust as needed)

-- 1. List all tables in the Glue database
SHOW TABLES IN supplychain_datalake;

-- 2. Preview first 10 rows of processed data
SELECT *
FROM supplychain_datalake.processed_test_data
LIMIT 10;

-- 3. Row count and basic statistics
SELECT
  COUNT(*) AS total_rows,
  MIN(demand) AS min_demand,
  MAX(demand) AS max_demand,
  AVG(demand) AS avg_demand
FROM supplychain_datalake.processed_test_data;

-- 4. Business insight: Top 10 parts with highest demand variability
SELECT
  part_id,
  STDDEV_POP(demand) AS demand_stddev,
  COUNT(*) AS records
FROM supplychain_datalake.processed_test_data
GROUP BY part_id
ORDER BY demand_stddev DESC
LIMIT 10;

-- 5. Cost optimization: Query using partition pruning (assuming partitioned by year and month)
SELECT
  part_id,
  SUM(demand) AS total_demand
FROM supplychain_datalake.processed_test_data
WHERE year = 2024 AND month = 6
GROUP BY part_id;

-- Note: Adjust table and column names as needed to match your schema. 