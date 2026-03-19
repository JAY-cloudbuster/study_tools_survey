# Pipeline Architecture

## Overview
The ETL pipeline follows a three-stage architecture:

### 1. Extract
- Baseline ETL: Initial data collection from survey responses
- Weekly ETL: Incremental data updates on a weekly schedule

### 2. Transform
- Data cleaning and validation
- Feature engineering
- Aggregation computations

### 3. Load
- PostgreSQL data warehouse
- Dashboard-ready datasets
- CSV exports for analysis

## Data Flow
```
Survey API -> Extract -> Transform -> PostgreSQL -> Dashboards
```
