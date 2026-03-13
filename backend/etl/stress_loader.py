import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "layer3_stress_dataset",
    "stress_students.csv"
)


def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def run_stress_loader():

    print("Loading stress dataset...")

    df = pd.read_csv(DATA_PATH)

    print(f"Rows read from CSV: {len(df)}")

    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO student_stress_context (
        study_hours,
        sleep_hours,
        academic_pressure,
        stress_level
    )
    VALUES (%s,%s,%s,%s)
    """

    rows_inserted = 0

    for _, row in df.iterrows():

        study_hours = int(row["stress_experience"])
        sleep_hours = int(row["sleep_problems"])
        academic_pressure = int(row["anxiety_tension"])
        stress_level = int(row["restlessness"])

        cur.execute(
            insert_query,
            (
                study_hours,
                sleep_hours,
                academic_pressure,
                stress_level
            )
        )

        rows_inserted += 1

    conn.commit()

    cur.close()
    conn.close()

    print(f"Inserted {rows_inserted} rows into student_stress_context table.")


if __name__ == "__main__":
    run_stress_loader()