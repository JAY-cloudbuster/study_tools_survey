import pandas as pd
from utils import get_db_connection

MAT_PATH = "../../data/layer2_student_performance/student-mat.csv"
POR_PATH = "../../data/layer2_student_performance/student-por.csv"


def run_student_performance_loader():

    print("Loading student performance datasets...")

    mat = pd.read_csv(MAT_PATH, sep=";")
    por = pd.read_csv(POR_PATH, sep=";")

    df = pd.concat([mat, por], ignore_index=True)

    print("Total rows loaded:", len(df))

    df = df[[
        "school",
        "sex",
        "age",
        "address",
        "famsize",
        "Pstatus",
        "Medu",
        "Fedu",
        "studytime",
        "failures",
        "absences",
        "internet",
        "activities",
        "G3"
    ]]

    df.rename(columns={"G3": "final_grade"}, inplace=True)

    conn = get_db_connection()
    cur = conn.cursor()

    inserted = 0

    for _, row in df.iterrows():

        cur.execute("""
        INSERT INTO student_performance(
            school,
            sex,
            age,
            address,
            famsize,
            Pstatus,
            Medu,
            Fedu,
            studytime,
            failures,
            absences,
            internet,
            activities,
            final_grade
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, tuple(row))

        inserted += 1

    conn.commit()

    cur.close()
    conn.close()

    print("Rows inserted:", inserted)


if __name__ == "__main__":
    run_student_performance_loader()