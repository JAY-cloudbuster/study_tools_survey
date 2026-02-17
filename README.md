# Study Tools Survey Analytics 
This is written so that:

A new person with zero context can reproduce everything

Every command is explicit

Every decision is justified

No tribal knowledge is required

You can copy–paste this as-is.

📊 Study Habits, Tools & Academic Performance
End-to-End Business Analytics Pipeline (India-wide Survey)
📌 Project Overview

This project builds a real-time, dynamic analytics pipeline to study how study habits and digital tool usage impact academic performance among university students in India.

Key characteristics:

Anonymous, cohort-based analytics (no personal identifiers)

Google Forms → Google Sheets → PostgreSQL → Analytics

Attention-check–validated data quality

Weekly time-series tracking

Designed for Power BI live dashboards

🧱 High-Level Architecture
Google Forms
   ↓
Google Sheets (Live)
   ↓
Python ETL (Attention-validated)
   ↓
PostgreSQL (Structured Storage)
   ↓
Analytics / Power BI (Next phase)

📁 Repository Structure
study_tools_survey/
│
├── backend/
│   ├── etl/
│   │   ├── baseline_etl.py
│   │   ├── weekly_etl.py
│   │   └── utils.py
│   │
│   ├── sql/
│   │   └── schema.sql
│   │
│   ├── .env              # NOT committed
│   ├── requirements.txt
│   └── venv/              # Virtual environment (ignored by Git)
│
├── .gitignore
└── README.md              # This file

🧠 Conceptual Design
1️⃣ Two Survey Types
Baseline Survey (One-time)

Captures:

Academic context (state, university type, course)

CGPA band

Baseline study habits

Regular digital tools used

Each response defines a cohort.

Weekly Survey (Repeated)

Captures:

Weekly study hours

Consistency, revision, stress

AI tool usage

Productivity

Constraints

Week number

This forms the time series.

2️⃣ No Personal Identifiers

No name, email, student ID collected

Cohorts are derived using hashed academic attributes

Privacy-safe analytics by design

🛠️ Technology Stack
Layer	Technology
Data Collection	Google Forms
Storage	Google Sheets
ETL	Python 3.11
Database	PostgreSQL
Analytics (next)	Power BI
Version Control	Git + GitHub
⚙️ Setup Instructions (From Scratch)
Step 1️⃣ Clone the Repository
git clone https://github.com/<your-username>/study_tools_survey.git
cd study_tools_survey

Step 2️⃣ Create Python Virtual Environment
cd backend
python -m venv venv


Activate it:

Windows (PowerShell):

venv\Scripts\activate


You should see:

(venv)

Step 3️⃣ Install Dependencies
pip install pandas psycopg2-binary python-dotenv
pip freeze > requirements.txt

🗄️ Database Setup (PostgreSQL)
Step 4️⃣ Create Database

Using pgAdmin or psql:

CREATE DATABASE study_analytics;

Step 5️⃣ Create Tables

Open pgAdmin → Query Tool, paste and run:

CREATE TABLE baseline_cohorts (
    cohort_key VARCHAR(128) PRIMARY KEY,
    state VARCHAR(100),
    university_type VARCHAR(100),
    course_program VARCHAR(150),
    year_of_study VARCHAR(50),
    cgpa_band VARCHAR(50),
    baseline_avg_daily_study_hours VARCHAR(50),
    digital_tools_raw TEXT,
    tool_count INT
);

CREATE TABLE weekly_observations (
    observation_id SERIAL PRIMARY KEY,
    cohort_key VARCHAR(128) REFERENCES baseline_cohorts(cohort_key),
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

🔐 Environment Configuration
Step 6️⃣ Create .env file

Inside backend/ create a file named .env:

DB_HOST=localhost
DB_NAME=study_analytics
DB_USER=postgres
DB_PASSWORD=your_password_here


⚠️ This file must never be committed.

🔄 ETL Pipeline (Core Logic)
Attention Check Enforcement

To ensure data quality:

Baseline survey accepts only "2–4 hours"

Weekly survey accepts only "ChatGPT / AI tools"

All other responses are discarded at ingestion.

Cohort Key Generation

A cohort is uniquely identified using:

State

University type

Course

CGPA band

These are:

Concatenated

SHA-256 hashed

Stored as cohort_key

This ensures:

No personal data

Stable grouping

Longitudinal tracking

▶️ Running the Pipeline
Step 7️⃣ Run Baseline ETL
cd backend
venv\Scripts\activate
python etl/baseline_etl.py


Expected output:

Baseline ETL completed.
Accepted rows: >0
Rejected rows: >0

Step 8️⃣ Run Weekly ETL
python etl/weekly_etl.py


Expected output:

Weekly ETL completed.
Accepted rows: >0
Rejected rows: >0

✅ Verification Checklist
Database Row Counts

In pgAdmin:

SELECT COUNT(*) FROM baseline_cohorts;
SELECT COUNT(*) FROM weekly_observations;


Both must be > 0.

Referential Integrity Check
SELECT COUNT(*)
FROM weekly_observations w
LEFT JOIN baseline_cohorts b
ON w.cohort_key = b.cohort_key
WHERE b.cohort_key IS NULL;


Expected:

0

🧪 What Has Been Fully Implemented

✔ Google Forms ingestion
✔ Live Google Sheets data source
✔ Attention-validated ETL
✔ PostgreSQL schema
✔ Cohort-based anonymization
✔ Weekly time-series storage
✔ Stable backend pipeline

🚀 Next Planned Steps (Not Yet Implemented)

Derived metrics (engagement, risk, momentum)

Power BI live dashboard

ETL automation (scheduler)

Documentation for analytics interpretation

🧠 Faculty-Ready Summary Statement

"This project implements an end-to-end, attention-validated analytics pipeline that ingests real-time Google Form survey data, enforces data quality at ingestion, and structures cohort-based weekly time-series data for scalable business analytics."

🧾 Troubleshooting Notes

Accepted rows = 0 → attention check mismatch

KeyError → column spacing issue (handled in code)

DB connection error → .env misconfigured

Timestamp issues → timestamps intentionally removed

🏁 Final Status

Backend pipeline is stable, verified, and production-ready.
This repository is now safe for:

Demonstration

Extension

Team collaboration

Analytics development
