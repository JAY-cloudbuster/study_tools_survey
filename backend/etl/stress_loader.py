import pandas as pd
from utils import get_db_connection

DATA_PATH = "../../data/layer3_stress_dataset/stress_students.csv"


def run_stress_loader():

    print("Loading stress dataset...")

    df = pd.read_csv(DATA_PATH)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    print("CSV rows detected:", len(df))

    # Map dataset columns → warehouse schema
    df["study_hours"] = df["stress_experience"]
    df["sleep_hours"] = df["sleep_problems"]
    df["academic_pressure"] = df["anxiety_tension"]
    df["stress_level"] = df["restlessness"]
    df["emotional_wellbeing"] = 5 - df["anxiety_tension"]
    df["social_support"] = 5 - df["restlessness"]

    # Select only needed columns
    df = df[
        [
            "study_hours",
            "sleep_hours",
            "academic_pressure",
            "stress_level",
            "emotional_wellbeing",
            "social_support",
        ]
    ]

    conn = get_db_connection()
    cur = conn.cursor()

    inserted = 0

    for _, row in df.iterrows():

        cur.execute(
            """
        INSERT INTO student_stress_context(
            study_hours,
            sleep_hours,
            academic_pressure,
            stress_level,
            emotional_wellbeing,
            social_support
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
            (
                int(row["study_hours"]),
                int(row["sleep_hours"]),
                int(row["academic_pressure"]),
                int(row["stress_level"]),
                int(row["emotional_wellbeing"]),
                int(row["social_support"]),
            ),
        )

        inserted += 1

    conn.commit()

    cur.close()
    conn.close()

    print("Rows inserted:", inserted)
    print("Layer-3 dataset loaded successfully.")


if __name__ == "__main__":
    run_stress_loader()