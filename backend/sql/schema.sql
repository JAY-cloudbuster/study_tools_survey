-- =====================================================
-- CLEAN REBUILD FOR CI
-- =====================================================

DROP TABLE IF EXISTS cohort_weekly_metrics CASCADE;
DROP TABLE IF EXISTS weekly_observations CASCADE;
DROP TABLE IF EXISTS baseline_cohorts CASCADE;
DROP TABLE IF EXISTS student_performance CASCADE;
DROP TABLE IF EXISTS student_stress_context CASCADE;



-- =====================================================
-- LAYER 1 — BASELINE COHORTS (SURVEY)
-- =====================================================

CREATE TABLE baseline_cohorts (

    cohort_key TEXT PRIMARY KEY,
    response_timestamp TIMESTAMP,

    state TEXT,
    university_type TEXT,
    course_program TEXT,
    year_of_study TEXT,
    cgpa_band TEXT,

    baseline_avg_daily_study_hours TEXT,

    digital_tools_raw TEXT,
    tool_count INT
);



-- =====================================================
-- LAYER 1 — WEEKLY OBSERVATIONS
-- =====================================================

CREATE TABLE weekly_observations (

    observation_id SERIAL PRIMARY KEY,

    cohort_key TEXT REFERENCES baseline_cohorts(cohort_key),

    response_timestamp TIMESTAMP,
    week_number TEXT,

    total_hours_this_week INT,
    avg_daily_study_hours TEXT,

    study_consistency TEXT,
    revision_frequency TEXT,
    group_study_participation TEXT,

    ai_tools_usage TEXT,
    approx_ai_usage_hours TEXT,
    digital_tool_usage_frequency TEXT,

    academic_constraints_raw TEXT,

    productivity_level INT,
    stress_level INT,

    had_assessment BOOLEAN,
    assessment_score INT,

    comparison_to_last_week TEXT,

    weekly_tools_raw TEXT
);



-- =====================================================
-- LAYER 2 — STUDENT PERFORMANCE DATASET (UCI)
-- =====================================================

CREATE TABLE student_performance (

    student_id SERIAL PRIMARY KEY,

    school TEXT,
    sex TEXT,
    age INT,
    address TEXT,

    famsize TEXT,
    Pstatus TEXT,

    Medu INT,
    Fedu INT,

    studytime INT,
    failures INT,
    absences INT,

    internet TEXT,
    activities TEXT,

    final_grade INT
);



-- =====================================================
-- LAYER 3 — STUDENT STRESS DATASET
-- =====================================================

CREATE TABLE student_stress_context (

    record_id SERIAL PRIMARY KEY,

    study_hours FLOAT,
    sleep_hours FLOAT,

    academic_pressure INT,
    stress_level INT,

    emotional_wellbeing INT,
    social_support INT
);



-- =====================================================
-- ANALYTICS TABLE
-- =====================================================

CREATE TABLE cohort_weekly_metrics (

    cohort_key TEXT,
    week_number TEXT,

    total_hours INT,
    avg_daily_hours_numeric FLOAT,

    num_tools_used_weekly INT,
    engagement_index FLOAT,

    productivity_level INT,
    stress_level INT,

    risk_flag TEXT,
    momentum TEXT,

    PRIMARY KEY (cohort_key, week_number)
);