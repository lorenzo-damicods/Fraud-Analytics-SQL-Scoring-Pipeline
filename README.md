# Fraud Analytics — SQL & Scoring Pipeline (PostgreSQL)

> **Short summary (5 seconds):**  
> Production-style fraud analytics pipeline in PostgreSQL: staging → dimensional modeling → analytical views, plus Python-based ML scoring ingestion and demo-ready outputs.

**PostgreSQL • SQL Data Modeling • Analytical Views • Python Scoring Ingestion**

---

## Overview

This repository shows how a credit-card fraud dataset can be transformed into a **fraud monitoring and reporting layer** using:
- a warehouse-style data model (staging + dimensions + fact),
- BI-ready analytical SQL views (monitoring, risk profiling, investigation queue),
- a Python script that simulates **model score ingestion** into PostgreSQL.

It complements a previous Fraud Detection project by focusing on **data engineering and operationalization**, rather than model training.

---

## 📁 Project Structure

```
Fraud-Analytics-SQL-Scoring-Pipeline/
│
├── assets/
│   ├── daily_monitoring_public.csv
│   ├── investigation_queue_public.csv
│   ├── expected_loss_top100_public.csv
│   ├── make_charts.py
│   ├── charts/
│   │   ├── 01_fraud_rate_over_time.png
│   │   ├── 02_expected_loss_distribution.png
│   │   ├── 03_top_segments_expected_loss.png
│   │   └── 04_top20_expected_loss.png
│   └── .keep
│
├── queries/
│   └── exploration.sql
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_load.sql
│   ├── 03_views.sql
│   └── 04_scoring_bridge.sql
│
├── write_scores.py
├── requirements.txt
└── README.md
```

---
## ✅ Demo Outputs (no dataset required)

If you just want to see the final results without running the pipeline, check `assets/`:

- `assets/expected_loss_top100_public.csv` — top 100 transactions ranked by expected loss (AED)
- `assets/investigation_queue_public.csv` — aggregated investigation queue (high-impact segments)
- `assets/daily_monitoring_public.csv` — daily monitoring KPIs (one row per date)

These files are **sanitized sample exports** generated from the final reporting SQL views (e.g., `fraud.v_expected_loss`, `fraud.v_daily_monitoring`, `fraud.v_investigation_queue`), they contain no direct identifiers and are provided for demo purposes.

## 📈 Charts

The repo also includes 4 presentation-ready charts generated from the reporting outputs:

- Fraud rate (%) over time (daily monitoring KPI)
- Expected loss distribution (log count)
- Top segments by total expected loss (geo + type + controls: 3DS/tokenization)
- Top 20 transactions by expected loss (triage list)

Charts are available under:
`assets/charts/`

To regenerate them locally (after exporting full CSVs from the DB), run:
```
python3 assets/make_charts.py
```

---
## 🗂️ Data Model Overview
The database follows a warehouse-style analytical design.

### Staging
- `fraud.stg_transactions`  
  Raw ingestion of the enhanced fraud dataset.

### Dimensions
- `fraud.dim_geo_area`
- `fraud.dim_customer`

### Fact table
- `fraud.fact_transactions` (partitioned by `transaction_date`)  
  Contains transaction features, labels, and engineered monitoring metrics, e.g.:
  - `is_fraud`
  - `cost_if_fraud`
  - `flag_over_50k`

### Scoring & monitoring tables
- `fraud.model_scores`
- `fraud.anomaly_scores`
- `fraud.alerts`

## 📊 Analytical Views

The reporting layer is exposed through BI-ready views:

- `fraud.v_fraud_rate_by_geo`
- `fraud.v_fraud_rate_by_controls`
- `fraud.v_daily_monitoring`
- `fraud.v_customer_risk_profile`
- `fraud.v_latest_model_score`
- `fraud.v_expected_loss`
- `fraud.v_investigation_queue`

The file `queries/exploration.sql` contains example queries to explore these outputs.

---

## 🚀 How to Run Locally (high level)

> **Note:** The raw dataset is **not included** in this repository due to size/licensing constraints.  
> The pipeline expects a CSV compatible with the schema defined in `sql/01_schema.sql`.


1️⃣ Create schema and tables
```
psql -h localhost -U <user> -d <database> -f sql/01_schema.sql
```
2️⃣ Load your CSV into staging
Replace the path with the location of your local CSV file (the dataset is not included in this repo).
```
\copy fraud.stg_transactions
FROM 'dataset/creditcard_enhanced_UAE_FINAL.csv'
CSV HEADER;

```
3️⃣ Populate dimensions and fact table
```
psql -h localhost -U <user> -d <database> -f sql/02_load.sql
```
4️⃣ Create scoring bridge view
```
psql -h localhost -U <user> -d <database> -f sql/04_scoring_bridge.sql
```
5️⃣ Ingest model scores (Python)
> Note: `write_scores.py` uses a demo score to illustrate operational score ingestion into PostgreSQL; any real model output can be plugged in.
```
python3 write_scores.py

```
6️⃣ Create analytical views
> Note: views can be created before or after score ingestion; they will reflect newly ingested scores.

```
psql -h localhost -U <user> -d <database> -f sql/03_views.sql
```
7️⃣ Run demo queries (optional)
```
psql -h localhost -U <user> -d <database> -f queries/exploration.sql
```
📦 Requirements

```
pandas
psycopg2-binary
```

🎯 Project Purpose

This project demonstrates my ability to:
- design production-style SQL data models (dimensional modeling + partitioned fact table),
- build a monitoring/reporting layer using analytical SQL views,
- operationalize ML outputs by ingesting risk scores into PostgreSQL,
- structure a maintainable, audit-friendly analytics pipeline.

Lorenzo D’Amico
Data Science Intern
