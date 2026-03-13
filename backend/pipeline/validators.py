def validate_study_hours(df):

    if (df["study_hours"] < 0).any():
        raise ValueError("Invalid study hours detected")


def validate_stress_level(df):

    if df["stress_level"].max() > 5:
        raise ValueError("Stress level outside allowed range")


def validate_null_ids(df):

    if df["student_id"].isnull().any():
        raise ValueError("Null student IDs detected")