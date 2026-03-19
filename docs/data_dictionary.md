# Data Dictionary

## Survey Response Fields

| Field | Type | Description |
|-------|------|-------------|
| response_id | INT | Unique identifier for each response |
| timestamp | DATETIME | When the response was submitted |
| tool_name | VARCHAR | Name of the study tool |
| rating | INT | User rating (1-5 scale) |
| frequency | VARCHAR | Usage frequency |
| effectiveness | INT | Perceived effectiveness score |

## Derived Fields

| Field | Type | Description |
|-------|------|-------------|
| week_number | INT | ISO week number |
| avg_rating | FLOAT | Weekly average rating |
| response_count | INT | Total responses per week |
