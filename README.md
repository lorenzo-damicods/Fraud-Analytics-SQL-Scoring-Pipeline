# Fraud Analytics SQL & Scoring Pipeline  
**PostgreSQL • SQL Data Modeling • Analytical Views • Python ML Scoring**

Production-style SQL analytics pipeline for fraud monitoring with PostgreSQL and Python-based ML scoring.

This project demonstrates how a credit card fraud dataset can be transformed into a **realistic fraud analytics and monitoring system**, combining SQL data modeling, analytical views, and Python-based model scoring.

It complements a previous Fraud Detection (EDA + SMOTE + ML) project by focusing on **data engineering and operationalisation**, rather than model training.

---

## 📁 Project Structure

fraud-analytics-sql-pipeline
│
├── 01_schema.sql
├── 02_load.sql
├── 03_views.sql
├── 04_scoring_bridge.sql
│
├── write_scores.py
├── queries/
│ └── exploration.sql
│
├── dataset/ # dataset not included
├── requirements.txt
└── README.md


---

## 🗂️ Data Model Overview

The database follows a **warehouse-style analytical design**.

### Staging
- `stg_transactions`  
  Raw ingestion of the enhanced fraud dataset.

### Dimensions
- `dim_geo_area`
- `dim_customer`

### Fact table
- `fact_transactions` (partitioned by `transaction_date`)  
  Contains transaction features, labels, and engineered business metrics such as:
  - `is_fraud`
  - `cost_if_fraud`
  - `flag_over_50k`

### Scoring & monitoring tables
- `model_scores`
- `anomaly_scores`
- `alerts`

---

## 📊 Analytical Views

The project exposes SQL views designed for **fraud monitoring and risk analysis**:

- `v_fraud_rate_by_geo`
- `v_fraud_rate_by_controls`
- `v_daily_monitoring`
- `v_customer_risk_profile`
- `v_latest_model_score`
- `v_expected_loss`
- `v_investigation_queue`

These views can be queried directly by analysts or connected to BI tools.

---

## 🚀 How to Run the Project

1️⃣ Create schema and tables
psql -h localhost -U <user> -d <database> -f 01_schema.sql

2️⃣ Load the CSV into staging
The dataset is not included due to size and licensing constraints.
\copy fraud.stg_transactions
FROM 'dataset/creditcard_enhanced_UAE_FINAL.csv'
CSV HEADER;

3️⃣ Populate dimensions and fact table
psql -h localhost -U <user> -d <database> -f 02_load.sql

4️⃣ Create analytical views
psql -h localhost -U <user> -d <database> -f 03_views.sql

5️⃣ Create scoring bridge view
psql -h localhost -U <user> -d <database> -f 04_scoring_bridge.sql

## Python ML Scoring Pipeline

The script write_scores.py simulates the ingestion of model predictions into the database.

It:
- loads the dataset
- assigns a placeholder fraud risk score (mock output)
- matches transactions using a scoring bridge view
- inserts results into fraud.model_scores

Environment variables (recommended)
export DB_HOST="localhost"
export DB_NAME="your_database"
export DB_USER="your_user"

Run the script
python write_scores.py

Credentials are intentionally not hardcoded and must be provided locally (e.g. via .pgpass or environment variables).

🔍 SQL Exploration:
- The file queries/exploration.sql contains example queries to explore:
- fraud rates by geography
- fraud rates by security controls (3DS, tokenization)
- daily fraud monitoring
- expected loss ranking
- investigation queue

## Requirements
pandas
psycopg2-binary


🎯 Project Purpose

This project demonstrates my ability to:
- design production-style SQL data models
- build fraud monitoring logic using pure SQL
- integrate Python-based ML scoring into a database
- structure a realistic, maintainable analytics pipeline

It is intended for Data Science, Fraud Analytics, and ML Engineering roles where SQL, data modeling, and ML operationalisation are required.

Lorenzo D’Amico
Data Science Intern
