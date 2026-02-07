import hashlib
import psycopg2

# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="study_analytics",
        user="postgres",
        password="YOUR_DB_PASSWORD"
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
