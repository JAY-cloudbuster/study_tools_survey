-- =====================================================
-- BASELINE COHORTS TABLE
-- Stores one-time academic + tool baseline data
-- =====================================================
CREATE TABLE baseline_cohorts (
    cohort_key VARCHAR(128) PRIMARY KEY,
    response_timestamp TIMESTAMP,

    state VARCHAR(50),
    university_type VARCHAR(50),
    course_program VARCHAR(100),
    year_of_study VARCHAR(20),
    cgpa_band VARCHAR(20),

    baseline_avg_daily_study_hours VARCHAR(20),

    digital_tools_raw TEXT,
    tool_count INT
);

-- =====================================================
-- WEEKLY OBSERVATIONS TABLE (TIME SERIES)
-- Stores repeated weekly behavior data
-- =====================================================
CREATE TABLE weekly_observations (
    observation_id SERIAL PRIMARY KEY,

    cohort_key VARCHAR(128),
    response_timestamp TIMESTAMP,

    week_number VARCHAR(20),

    total_hours_this_week INT,
    avg_daily_study_hours VARCHAR(20),

    study_consistency VARCHAR(50),
    revision_frequency VARCHAR(50),
    group_study_participation VARCHAR(50),

    ai_tools_usage VARCHAR(100),
    approx_ai_usage_hours VARCHAR(20),
    digital_tool_usage_frequency VARCHAR(50),

    academic_constraints_raw TEXT,

    productivity_level INT,
    stress_level INT,

    had_assessment BOOLEAN,
    assessment_score INT,

    comparison_to_last_week VARCHAR(50),

    weekly_tools_raw TEXT,

    CONSTRAINT fk_baseline_cohort
        FOREIGN KEY (cohort_key)
        REFERENCES baseline_cohorts(cohort_key)
);

-- =====================================================
-- DERIVED BUSINESS METRICS TABLE
-- Stores analytics-ready computed indicators
-- =====================================================
CREATE TABLE cohort_weekly_metrics (
    cohort_key VARCHAR(128),
    week_number VARCHAR(20),

    total_hours INT,
    avg_daily_hours_numeric FLOAT,

    num_tools_used_weekly INT,
    engagement_index FLOAT,

    productivity_level INT,
    stress_level INT,

    risk_flag VARCHAR(20),
    comparison_trend VARCHAR(50),

    PRIMARY KEY (cohort_key, week_number)
);
