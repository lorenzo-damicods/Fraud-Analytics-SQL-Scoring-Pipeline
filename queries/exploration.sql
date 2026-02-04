-- Quick exploration / sanity checks after running the pipeline
-- Usage: run inside psql after creating schema, loading data, ingesting scores, and creating views.

SET search_path TO fraud;

-- Row counts (sanity checks)
SELECT COUNT(*) AS stg_transactions_rows FROM stg_transactions;
SELECT COUNT(*) AS fact_transactions_rows FROM fact_transactions;

-- Quick view samples
SELECT * FROM v_fraud_rate_by_geo LIMIT 10;
SELECT * FROM v_fraud_rate_by_controls LIMIT 10;
SELECT * FROM v_daily_monitoring LIMIT 10;

-- Top expected loss (transaction-level)
SELECT *
FROM v_expected_loss
ORDER BY expected_loss_aed DESC
LIMIT 20;
