import hashlib
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
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
# Cohort Key Generator
# -----------------------------
def generate_cohort_key(row):
    raw_key = (
        str(row["State"]) +
        str(row["Type of university"]) +
        str(row["Course / Program"]) +
        str(row["Current CGPA band"])
    )
    return hashlib.sha256(raw_key.encode()).hexdigest()
