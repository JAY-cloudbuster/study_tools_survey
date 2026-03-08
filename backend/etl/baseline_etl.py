import pandas as pd
from utils import get_db_connection, generate_cohort_key

BASELINE_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "19cPgZ0sf23MCRknkdxliMp-HBa1BS1_ffWjcqmmNPJA"
    "/export?format=csv"
)

def normalize(text):
    return (
        str(text).lower()
        .replace("–", "-")
        .replace("—", "-")
        .replace(" ", "")
    )

def is_valid_attention(text):
    return normalize(text).startswith("2-4")


def run_baseline_etl():

    df = pd.read_csv(BASELINE_SHEET_URL)
    df.columns = df.columns.str.strip()

    # Convert timestamp to PostgreSQL compatible format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    attention_col = next(
        col for col in df.columns if "attention check" in col.lower()
    )

    conn = get_db_connection()
    cur = conn.cursor()

    accepted = 0
    rejected = 0

    for _, row in df.iterrows():

        if not is_valid_attention(row.get(attention_col, "")):
            rejected += 1
            continue

        cohort_key = generate_cohort_key(row)

        cur.execute("""
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
        """, (
            cohort_key,
            row["Timestamp"],
            row.get("Which state are you currently studying in?"),
            row.get("Type of university / institution"),
            row.get("Course / Program"),
            row.get("Current year of study"),
            row.get("Your current CGPA band (at the start of this study)"),
            row.get("On average, how many hours did you usually study per day before this study?"),
            row.get("Which digital tools do you regularly use? (Select all that apply)"),
            row.get("Validation Follow-up  \nHow many options did you select in the previous question?")
        ))

        accepted += 1

    conn.commit()
    cur.close()
    conn.close()

    print("Baseline ETL completed.")
    print(f"Accepted rows: {accepted}")
    print(f"Rejected rows: {rejected}")


if __name__ == "__main__":
    run_baseline_etl()