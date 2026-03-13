-- =====================================================
-- ENGAGEMENT METRICS VIEW
-- Computes engagement index from productivity & stress
-- =====================================================

DROP MATERIALIZED VIEW IF EXISTS engagement_metrics;

CREATE MATERIALIZED VIEW engagement_metrics AS
SELECT
    cohort_key,
    week_number,
    total_hours_this_week,
    productivity_level,
    stress_level,

    (productivity_level * 0.7 + (10 - stress_level) * 0.3)
    AS engagement_index

FROM weekly_observations;



-- =====================================================
-- ACADEMIC RISK ANALYSIS VIEW
-- Flags students at academic risk
-- =====================================================

DROP MATERIALIZED VIEW IF EXISTS academic_risk_analysis;

CREATE MATERIALIZED VIEW academic_risk_analysis AS
SELECT
    cohort_key,
    week_number,
    total_hours_this_week,
    productivity_level,
    stress_level,

    CASE
        WHEN stress_level >= 4 AND total_hours_this_week < 15
        THEN 'HIGH_RISK'

        WHEN stress_level >= 3
        THEN 'MEDIUM_RISK'

        ELSE 'LOW_RISK'
    END AS risk_category

FROM weekly_observations;



-- =====================================================
-- TOOL ADOPTION ANALYSIS
-- Segments students by tool usage
-- =====================================================

DROP MATERIALIZED VIEW IF EXISTS tool_adoption_analysis;

CREATE MATERIALIZED VIEW tool_adoption_analysis AS
SELECT
    state,
    university_type,
    course_program,

    COUNT(*) AS student_count,
    AVG(tool_count) AS avg_tools_used

FROM baseline_cohorts
GROUP BY state, university_type, course_program;



-- =====================================================
-- STRESS BEHAVIOR ANALYSIS
-- Behavioral indicators from stress dataset
-- =====================================================

DROP MATERIALIZED VIEW IF EXISTS stress_behavior_analysis;

CREATE MATERIALIZED VIEW stress_behavior_analysis AS
SELECT
    study_hours,
    sleep_hours,
    academic_pressure,
    stress_level

FROM student_stress_context;