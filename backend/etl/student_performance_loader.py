import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()


# ---------------------------------------------------
# Resolve project root dynamically
# ---------------------------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATA_DIR = os.path.join(BASE_DIR, "data", "layer2_student_performance")

MAT_PATH = os.path.join(DATA_DIR, "student-mat.csv")
POR_PATH = os.path.join(DATA_DIR, "student-por.csv")


# ---------------------------------------------------
# Database connection
# ---------------------------------------------------

def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# ---------------------------------------------------
# Loader Function
# ---------------------------------------------------

def run_student_performance_loader():

    print("Loading student performance datasets...")

    # Load datasets
    mat = pd.read_csv(MAT_PATH, sep=";")
    por = pd.read_csv(POR_PATH, sep=";")

    mat["course"] = "math"
    por["course"] = "portuguese"

    df = pd.concat([mat, por], ignore_index=True)

    print(f"Total records loaded from CSV: {len(df)}")

    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO student_performance (
        school,
        sex,
        age,
        address,
        famsize,
        Pstatus,
        Medu,
        Fedu,
        Mjob,
        Fjob,
        reason,
        guardian,
        traveltime,
        studytime,
        failures,
        schoolsup,
        famsup,
        paid,
        activities,
        nursery,
        higher,
        internet,
        romantic,
        famrel,
        freetime,
        goout,
        Dalc,
        Walc,
        health,
        absences,
        G1,
        G2,
        G3,
        course
    )
    VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s
    )
    """

    rows_inserted = 0

    for _, row in df.iterrows():

        values = tuple(row[col] for col in df.columns)

        cur.execute(insert_query, values)
        rows_inserted += 1

    conn.commit()

    cur.close()
    conn.close()

    print(f"Inserted {rows_inserted} rows into student_performance table.")


# ---------------------------------------------------

if __name__ == "__main__":
    run_student_performance_loader()