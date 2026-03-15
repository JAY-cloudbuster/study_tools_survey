# 📊 Study Habits, Digital Tools & Academic Performance
## End-to-End Student Behavior Analytics Platform

This project implements a **complete data engineering and analytics pipeline** designed to analyze how **study habits, stress levels, and digital learning tools influence student productivity and academic outcomes.**

The system integrates multiple datasets, performs automated ETL processing, stores structured data in a **PostgreSQL data warehouse**, and produces analytical insights through **Tableau dashboards**.

The project demonstrates a **production-style analytics architecture** combining **data engineering, SQL analytics, and business intelligence visualization.**

---

# 🎯 Project Objectives

The primary goal of this project is to build a **data-driven analytics platform** capable of identifying behavioral patterns in student learning.

The platform analyzes relationships between:

- Study hours
- Study consistency
- Stress levels
- Digital tool usage
- AI tool adoption
- Academic performance indicators

The final system enables **behavioral analytics and educational insights** that help identify:

- High engagement students
- Students at academic risk
- Impact of digital tools on productivity
- Stress-productivity relationships
- Study behavior trends over time

---

# 🧱 High-Level System Architecture
CSV / Survey Datasets
↓
Python ETL Pipelines
↓
PostgreSQL Data Warehouse
↓
SQL Analytical Views
↓
Tableau Dashboard

The architecture follows a **modern analytics pipeline structure**, similar to those used in real-world data teams.

---

# 🧠 Core Design Principles

### 1️⃣ Behavioral Analytics

The platform focuses on **student behavior rather than only final grades**, allowing deeper understanding of:

- learning habits
- productivity fluctuations
- stress impact
- digital tool usage

---

### 2️⃣ Multi-Dataset Integration

The platform integrates multiple datasets:

| Dataset | Purpose |
|------|------|
| Student Study Survey | Weekly study behavior |
| Student Performance Dataset | Academic performance indicators |
| Student Stress Dataset | Psychological and lifestyle indicators |

---

### 3️⃣ Data Engineering Pipeline

The project implements a **modular ETL pipeline** that performs:

- Data ingestion
- Data cleaning
- Schema alignment
- Data validation
- Warehouse loading

---

# 🛠 Technology Stack

| Layer | Technology |
|------|------|
| Data Processing | Python |
| Data Analysis | Pandas |
| ETL Pipeline | Custom Python Scripts |
| Database | PostgreSQL |
| SQL Analytics | PostgreSQL Views |
| Visualization | Tableau |
| Version Control | Git + GitHub |
| CI/CD | GitHub Actions |
| Environment Management | Python venv |

---

# 📁 Repository Structure

The architecture follows a **modern analytics pipeline structure**, similar to those used in real-world data teams.

---

# 🧠 Core Design Principles

### 1️⃣ Behavioral Analytics

The platform focuses on **student behavior rather than only final grades**, allowing deeper understanding of:

- learning habits
- productivity fluctuations
- stress impact
- digital tool usage

---

### 2️⃣ Multi-Dataset Integration

The platform integrates multiple datasets:

| Dataset | Purpose |
|------|------|
| Student Study Survey | Weekly study behavior |
| Student Performance Dataset | Academic performance indicators |
| Student Stress Dataset | Psychological and lifestyle indicators |

---

### 3️⃣ Data Engineering Pipeline

The project implements a **modular ETL pipeline** that performs:

- Data ingestion
- Data cleaning
- Schema alignment
- Data validation
- Warehouse loading

---

# 🛠 Technology Stack

| Layer | Technology |
|------|------|
| Data Processing | Python |
| Data Analysis | Pandas |
| ETL Pipeline | Custom Python Scripts |
| Database | PostgreSQL |
| SQL Analytics | PostgreSQL Views |
| Visualization | Tableau |
| Version Control | Git + GitHub |
| CI/CD | GitHub Actions |
| Environment Management | Python venv |

---

# 📁 Repository Structure
study_tools_survey
│
├── backend
│
│ ├── etl
│ │ baseline_etl.py
│ │ weekly_etl.py
│ │ student_performance_loader.py
│ │ stress_loader.py
│ │ utils.py
│ │
│ ├── pipeline
│ │ orchestrator.py
│ │
│ ├── sql
│ │ schema.sql
│ │ analytics_views.sql
│ │ refresh_views.sql
│ │
│ ├── run_pipeline.py
│ └── requirements.txt
│
├── data
│ ├── layer2_student_performance
│ │ student-mat.csv
│ │ student-por.csv
│ │
│ └── layer3_stress_dataset
│ stress_students.csv
│
├── dashboards
│ study_behavior_dashboard.twb
│
├── .github
│ workflows
│ pipeline.yml
│
└── README.md

---

# 🗄 Data Warehouse Design

The PostgreSQL warehouse contains multiple relational tables designed for behavioral analytics.

### Main Tables

| Table | Description |
|------|------|
| baseline_cohorts | Student baseline academic context |
| weekly_observations | Weekly behavioral survey responses |
| student_performance | External academic performance dataset |
| student_stress_context | Student lifestyle and stress dataset |
| cohort_weekly_metrics | Derived analytics table |

---

### Example Schema
baseline_cohorts
│
└── cohort_key
│
▼
weekly_observations

student_performance
student_stress_context

The schema allows:

- cohort-level analysis
- weekly behavioral tracking
- multi-dataset correlation

---

# 🔄 ETL Pipeline

The ETL pipeline is implemented in **Python** and consists of several modular scripts.

### Baseline ETL
Processes baseline survey responses and loads them into:
### Weekly ETL
Processes weekly behavioral survey responses and loads them into:

---

### Student Performance Dataset Loader

Loads external academic performance dataset.

---

### Student Stress Dataset Loader

Loads psychological and lifestyle dataset.

---

# ⚙ Pipeline Orchestration

To simplify execution, the entire ETL workflow can be executed using a single command.

The orchestrator performs:

1️⃣ Baseline ETL  
2️⃣ Weekly ETL  
3️⃣ Student performance dataset load  
4️⃣ Stress dataset load  
5️⃣ SQL analytics refresh  

---

# 📊 Analytical SQL Layer

The analytics layer generates behavioral insights through SQL views.

### Engagement Index
engagement_index =
productivity_level * 0.7 +
(10 - stress_level) * 0.3
---

### Academic Risk Classification
CASE
WHEN stress_level >= 4 AND total_hours_this_week < 15
THEN 'HIGH_RISK'

WHEN stress_level >= 3
THEN 'MEDIUM_RISK'

ELSE 'LOW_RISK'
END

---

### Analytics Views

| View | Purpose |
|------|------|
| engagement_metrics | Student engagement score |
| academic_risk_analysis | Risk classification |
| tool_adoption_analysis | Digital tool usage patterns |
| stress_behavior_analysis | Stress behavior relationships |

---

# 📊 Tableau Dashboard

The final analytics results are visualized using **Tableau**.

The dashboard includes:

### KPI Cards

- Total Students
- Average Study Hours
- Average Productivity
- Average Stress

---

### Visualizations

- Study Hours vs Productivity
- Stress vs Productivity
- Academic Risk Distribution
- Digital Tool Adoption by Program
- Weekly Engagement Trends

---

### Interactive Filters

Users can filter results by:

- Course program
- University type
- State
- Risk category

---

# ⚡ Automation

The project supports automated execution of the ETL pipeline.

Automation features include:

- Pipeline orchestration script
- Automated SQL view refresh
- Scheduled pipeline execution
- Logging support

---

# 🔁 CI/CD Pipeline

The repository includes a **GitHub Actions workflow** that validates the pipeline.

The CI pipeline performs:

1️⃣ Install dependencies  
2️⃣ Run ETL scripts  
3️⃣ Validate database connections  
4️⃣ Execute analytics SQL  

This ensures the pipeline remains stable during development.

---

# 🧪 Example Pipeline Output
