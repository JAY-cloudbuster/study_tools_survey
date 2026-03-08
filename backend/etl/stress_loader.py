import pandas as pd
from utils import get_db_connection

DATA_PATH = "../../data/layer3_stress_dataset/stress_students.csv"


def run_stress_loader():

    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    conn = get_db_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():

        cur.execute("""
        INSERT INTO student_stress_context(
            study_hours,
            sleep_hours,
            academic_pressure,
            stress_level,
            emotional_wellbeing,
            social_support
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            row.get("study_hours"),
            row.get("sleep_hours"),
            row.get("academic_pressure"),
            row.get("stress_level"),
            row.get("emotional_wellbeing"),
            row.get("social_support")
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Layer-3 dataset loaded successfully.")


if __name__ == "__main__":
    run_stress_loader()