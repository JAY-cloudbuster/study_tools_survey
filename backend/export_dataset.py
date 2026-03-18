import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# DB connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# -------- LOAD TABLES -------- #

baseline = pd.read_sql("SELECT * FROM baseline_cohorts;", conn)
weekly = pd.read_sql("SELECT * FROM weekly_observations;", conn)

# Optional: if analytics table exists
try:
    metrics = pd.read_sql("SELECT * FROM cohort_weekly_metrics;", conn)
    use_metrics = True
except:
    use_metrics = False

# -------- MERGE CORE -------- #

merged = weekly.merge(baseline, on="cohort_key", how="left")

# -------- ADD ANALYTICS (if exists) -------- #

if use_metrics:
    merged = merged.merge(metrics, on=["cohort_key", "week_number"], how="left")

# -------- SAVE FINAL DATASET -------- #

merged.to_csv("final_dataset.csv", index=False)

print("Dataset exported successfully: final_dataset.csv")
print("Rows:", merged.shape[0])
print("Columns:", merged.shape[1])