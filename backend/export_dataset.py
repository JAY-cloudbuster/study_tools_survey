# ============================================================
# export_dataset.py
# Purpose:
#   Extract the dataset used by the dashboard directly from
#   PostgreSQL, merge baseline + weekly tables, apply
#   submission-safe cleaning, and export a single CSV.
#
# Requirements:
#   - backend/.env must contain DB credentials
#   - Tables must exist:
#       baseline_cohorts
#       weekly_observations
#
# Output:
#   backend/final_dataset.csv         (raw merged)
#   backend/final_dataset_clean.csv   (cleaned for submission)
# ============================================================

import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# ------------------------------------------------------------
# 1) LOAD ENVIRONMENT VARIABLES
# ------------------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("Missing DB credentials in .env")

# ------------------------------------------------------------
# 2) CONNECT TO DATABASE
# ------------------------------------------------------------
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# ------------------------------------------------------------
# 3) LOAD TABLES
# ------------------------------------------------------------
baseline_query = "SELECT * FROM baseline_cohorts;"
weekly_query = "SELECT * FROM weekly_observations;"

baseline = pd.read_sql(baseline_query, conn)
weekly = pd.read_sql(weekly_query, conn)

conn.close()

# ------------------------------------------------------------
# 4) BASIC SANITY CLEANING
# ------------------------------------------------------------
baseline.columns = baseline.columns.str.strip()
weekly.columns = weekly.columns.str.strip()

# ------------------------------------------------------------
# 5) MERGE CORE DATA (SOURCE OF TRUTH)
# ------------------------------------------------------------
merged = weekly.merge(baseline, on="cohort_key", how="left")

# ------------------------------------------------------------
# 6) SAVE RAW DATASET (UNTOUCHED)
# ------------------------------------------------------------
output_raw_path = os.path.join(os.getcwd(), "final_dataset.csv")
merged.to_csv(output_raw_path, index=False)

# ------------------------------------------------------------
# 7) CLEANING STRATEGY (SUBMISSION SAFE)
# ------------------------------------------------------------
df_clean = merged.copy()

# --- Categorical defaults ---
df_clean["ai_tools_usage"] = df_clean["ai_tools_usage"].fillna("Not Used")
df_clean["weekly_tools_raw"] = df_clean["weekly_tools_raw"].fillna("None")
df_clean["digital_tools_raw"] = df_clean["digital_tools_raw"].fillna("None")
df_clean["academic_constraints_raw"] = df_clean["academic_constraints_raw"].fillna("None")

# --- Conditional numeric ---
# If no assessment → score = 0
df_clean["assessment_score"] = df_clean["assessment_score"].fillna(0)

# --- Optional normalization flags (do NOT change original meaning) ---
df_clean["used_ai"] = df_clean["ai_tools_usage"].apply(
    lambda x: 0 if x == "Not Used" else 1
)

df_clean["has_constraints"] = df_clean["academic_constraints_raw"].apply(
    lambda x: 0 if x == "None" else 1
)

# ------------------------------------------------------------
# 8) FINAL EXPORT (CLEAN DATASET)
# ------------------------------------------------------------
output_clean_path = os.path.join(os.getcwd(), "final_dataset_clean.csv")
df_clean.to_csv(output_clean_path, index=False)

# ------------------------------------------------------------
# 9) VALIDATION PRINTS
# ------------------------------------------------------------
print("\n================ EXPORT SUMMARY ================\n")
print("Raw dataset saved at:", output_raw_path)
print("Clean dataset saved at:", output_clean_path)

print("\nShape (rows, columns):", df_clean.shape)

print("\nMissing values after cleaning:\n")
print(df_clean.isna().sum())

print("\n================================================\n")