import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATA_DIR = os.path.join(BASE_DIR, "data", "layer2_student_performance")

MAT_PATH = os.path.join(DATA_DIR, "student-mat.csv")
POR_PATH = os.path.join(DATA_DIR, "student-por.csv")


def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def run_student_performance_loader():

    print("Loading student performance datasets...")

    mat = pd.read_csv(MAT_PATH, sep=";")
    por = pd.read_csv(POR_PATH, sep=";")

    mat["course"] = "math"
    por["course"] = "portuguese"

    df = pd.concat([mat, por], ignore_index=True)

    print(f"Total records loaded from CSV: {len(df)}")

    # Keep only analytics columns
    df = df[
        [
            "studytime",
            "failures",
            "absences",
            "G1",
            "G2",
            "G3",
            "course",
        ]
    ]

    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO student_performance (
        studytime,
        failures,
        absences,
        g1,
        g2,
        g3,
        course
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    rows_inserted = 0

    for _, row in df.iterrows():

        cur.execute(
            insert_query,
            (
                int(row["studytime"]),
                int(row["failures"]),
                int(row["absences"]),
                int(row["G1"]),
                int(row["G2"]),
                int(row["G3"]),
                row["course"],
            ),
        )

        rows_inserted += 1

    conn.commit()

    cur.close()
    conn.close()

    print(f"Inserted {rows_inserted} rows into student_performance table.")


if __name__ == "__main__":
    run_student_performance_loader()