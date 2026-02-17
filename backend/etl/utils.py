import hashlib
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# -----------------------------
# Safe column getter
# -----------------------------
def get_col(row, col_name):
    """
    Safely fetch a column even if Google Forms
    adds leading/trailing spaces.
    """
    for key in row.index:
        if key.strip() == col_name:
            return row[key]
    raise KeyError(f"Column not found: {col_name}")

# -----------------------------
# Cohort Key Generator (SAFE)
# -----------------------------
def generate_cohort_key(row):
    raw_key = (
        str(get_col(row, "Which state are you currently studying in?")) +
        str(get_col(row, "Type of university / institution")) +
        str(get_col(row, "Course / Program")) +
        str(get_col(row, "Your current CGPA band (at the start of this study)"))
    )
    return hashlib.sha256(raw_key.encode()).hexdigest()
