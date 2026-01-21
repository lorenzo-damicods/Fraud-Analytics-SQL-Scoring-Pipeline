import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

CSV_PATH = os.getenv("CSV_PATH", "dataset/creditcard_enhanced_UAE_FINAL.csv")

df = pd.read_csv(CSV_PATH)

# TODO: replace with your model output (predict_proba)
df["risk_score"] = 0.5

threshold_used = float(os.getenv("THRESHOLD", "0.80"))
model_version = os.getenv("MODEL_VERSION", "xgb_v1")
df["flag_xgb"] = df["risk_score"] >= threshold_used

# Build a minimal key for matching DB rows + carry score columns safely
keys = df[["Time", "customer_id", "Amount", "risk_score", "flag_xgb"]].copy()
keys.columns = ["time_seconds", "customer_id", "amount", "risk_score", "flag_xgb"]

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    dbname=os.getenv("DB_NAME", "try"),
    user=os.getenv("DB_USER", "user")
)
conn.autocommit = False

bridge_query = """
SELECT transaction_id, transaction_date, time_seconds, customer_id, amount
FROM fraud.v_scoring_bridge;
"""

bridge = pd.read_sql(bridge_query, conn)

merged = keys.merge(
    bridge,
    on=["time_seconds", "customer_id", "amount"],
    how="inner"
)

merged["threshold_used"] = threshold_used
merged["model_version"] = model_version

rows = list(
    merged[["transaction_id", "transaction_date", "model_version", "risk_score", "threshold_used", "flag_xgb"]]
    .itertuples(index=False, name=None)
)

insert_sql = """
INSERT INTO fraud.model_scores
(transaction_id, transaction_date, model_version, risk_score, threshold_used, flag_xgb)
VALUES %s;
"""

with conn.cursor() as cur:
    execute_values(cur, insert_sql, rows, page_size=10000)

conn.commit()
conn.close()

print("Inserted rows into fraud.model_scores:", len(rows))
