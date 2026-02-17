-- =====================================================
-- BASELINE COHORTS TABLE
-- Stores one-time academic baseline data
-- =====================================================
CREATE TABLE IF NOT EXISTS baseline_cohorts (
    cohort_key VARCHAR(128) PRIMARY KEY,

    response_timestamp TIMESTAMP,

    state VARCHAR(100),
    university_type VARCHAR(100),
    course_program VARCHAR(150),
    year_of_study VARCHAR(50),
    cgpa_band VARCHAR(50),

    baseline_avg_daily_study_hours VARCHAR(50),

    digital_tools_raw TEXT,
    tool_count INT
);

-- =====================================================
-- WEEKLY OBSERVATIONS TABLE (TIME-SERIES FACT TABLE)
-- Stores weekly study behavior data
-- =====================================================
CREATE TABLE IF NOT EXISTS weekly_observations (
    observation_id SERIAL PRIMARY KEY,

    cohort_key VARCHAR(128) REFERENCES baseline_cohorts(cohort_key),

    response_timestamp TIMESTAMP,
    week_number VARCHAR(50),

    total_hours_this_week INT,
    avg_daily_study_hours VARCHAR(50),

    study_consistency VARCHAR(100),
    revision_frequency VARCHAR(100),
    group_study_participation VARCHAR(100),

    ai_tools_usage VARCHAR(150),
    approx_ai_usage_hours VARCHAR(50),
    digital_tool_usage_frequency VARCHAR(100),

    academic_constraints_raw TEXT,

    productivity_level INT,
    stress_level INT,

    had_assessment BOOLEAN,
    assessment_score INT,

    comparison_to_last_week VARCHAR(150),

    weekly_tools_raw TEXT
);

-- =====================================================
-- DERIVED METRICS TABLE
-- Stores analytics-ready computed indicators
-- =====================================================
CREATE TABLE IF NOT EXISTS cohort_weekly_metrics (
    cohort_key VARCHAR(128),
    week_number VARCHAR(50),

    total_hours INT,
    avg_daily_hours_numeric FLOAT,

    num_tools_used_weekly INT,
    engagement_index FLOAT,

    productivity_level INT,
    stress_level INT,

    risk_flag VARCHAR(50),
    momentum VARCHAR(50),

    PRIMARY KEY (cohort_key, week_number)
);
