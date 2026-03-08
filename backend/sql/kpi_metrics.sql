CREATE OR REPLACE VIEW dashboard_kpis AS
SELECT
    COUNT(DISTINCT cohort_key) AS total_students,
    AVG(total_hours_this_week) AS avg_weekly_study_hours,
    AVG(productivity_level) AS avg_productivity,
    AVG(stress_level) AS avg_stress,
    AVG(productivity_level * 0.7 + (10 - stress_level) * 0.3) AS avg_engagement
FROM weekly_observations;