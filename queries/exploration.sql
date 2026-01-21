SELECT COUNT(*) FROM fraud.stg_transactions;
SELECT COUNT(*) FROM fraud.fact_transactions;
SELECT * FROM fraud.v_fraud_rate_by_geo LIMIT 10;
SELECT * FROM fraud.v_fraud_rate_by_controls LIMIT 10;
SELECT * FROM fraud.v_daily_monitoring LIMIT 10;
SELECT * FROM fraud.v_expected_loss ORDER BY expected_loss_aed DESC LIMIT 20;
