import pandas as pd
from utils import get_db_connection, generate_cohort_key

# -----------------------------
# Google Sheet CSV URL (Baseline)
# -----------------------------
BASELINE_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "19cPgZ0sf23MCRknkdxliMp-HBa1BS1_ffWjcqmmNPJA"
    "/export?format=csv"
)

def run_baseline_etl():
    df = pd.read_csv(BASELINE_SHEET_URL)

    conn = get_db_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cohort_key = generate_cohort_key(row)

        query = """
        INSERT INTO baseline_cohorts (
            cohort_key,
            response_timestamp,
            state,
            university_type,
            course_program,
            year_of_study,
            cgpa_band,
            baseline_avg_daily_study_hours,
            digital_tools_raw,
            tool_count
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (cohort_key) DO NOTHING;
        """

        cur.execute(query, (
            cohort_key,
            row["Timestamp"],
            row["State"],
            row["Type of university"],
            row["Course / Program"],
            row["Current year of study"],
            row["Current CGPA band"],
            row["Hours usually studied per day before study"],
            row["Which digital tools do you regularly use?"],
            row["Count of tools selected"]
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("Baseline ETL completed successfully.")

if __name__ == "__main__":
    run_baseline_etl()
