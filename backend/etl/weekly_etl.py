import pandas as pd
import random
import re
from utils import get_db_connection

WEEKLY_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1LIf88WLUMoBtnldla_6PwXqFUIw3xPNOaer3E4dSxVI"
    "/export?format=csv"
)


def parse_int(value):
    """
    Safely extract an integer from survey responses.

    Handles formats like:
    '8'
    '8-10'
    '10+'
    '5 hours'
    '7/10'
    """

    if value is None:
        return None

    value = str(value)

    match = re.search(r'\d+', value)

    if match:
        return int(match.group())

    return None


def run_weekly_etl():

    df = pd.read_csv(WEEKLY_SHEET_URL)

    # Normalize column names
    df.columns = df.columns.str.strip()

    # Convert timestamps
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # Detect attention check column
    attention_col = next(
        col for col in df.columns if "answering carefully" in col.lower()
    )

    conn = get_db_connection()
    cur = conn.cursor()

    # Load cohort keys from baseline table
    cur.execute("SELECT cohort_key FROM baseline_cohorts;")
    cohort_keys = [row[0] for row in cur.fetchall()]

    if not cohort_keys:
        raise RuntimeError("No baseline cohorts found. Run baseline ETL first.")

    accepted = 0
    rejected = 0

    for _, row in df.iterrows():

        # Filter invalid responses
        if "chatgpt" not in str(row.get(attention_col, "")).lower():
            rejected += 1
            continue

        # Random cohort assignment
        cohort_key = random.choice(cohort_keys)

        cur.execute("""
        INSERT INTO weekly_observations (
            cohort_key,
            response_timestamp,
            week_number,
            total_hours_this_week,
            avg_daily_study_hours,
            study_consistency,
            revision_frequency,
            group_study_participation,
            ai_tools_usage,
            approx_ai_usage_hours,
            digital_tool_usage_frequency,
            academic_constraints_raw,
            productivity_level,
            stress_level,
            had_assessment,
            assessment_score,
            comparison_to_last_week,
            weekly_tools_raw
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (
            cohort_key,
            row["Timestamp"],
            row.get("Week Number"),

            parse_int(row.get("Total number of hours you studied in the past 7 days")),

            row.get("Average daily study hours during weekdays this week"),
            row.get("How consistent was your study routine THIS WEEK?"),
            row.get("How often did you revise material within 24 hours THIS WEEK?"),
            row.get("Group study participation THIS WEEK"),
            row.get("AI Tools Usage"),
            row.get("Approximate hours spent using AI tools THIS WEEK"),
            row.get("Overall frequency of digital tool usage THIS WEEK"),
            row.get("Did you face any constraints THIS WEEK? (Select all that apply)"),

            parse_int(row.get("Your productivity level THIS WEEK")),
            parse_int(row.get("Your academic stress level THIS WEEK")),

            str(row.get("Did you have any academic assessment THIS WEEK?")).lower() == "yes",

            parse_int(row.get("If yes, approximate score (%)")),

            row.get("Compared to LAST WEEK, your overall study effectiveness is:"),
            row.get("Which of the following learning tools did you use THIS WEEK? (Select all that apply)")
        ))

        accepted += 1

    conn.commit()
    cur.close()
    conn.close()

    print("Weekly ETL completed.")
    print(f"Accepted rows: {accepted}")
    print(f"Rejected rows: {rejected}")


if __name__ == "__main__":
    run_weekly_etl()