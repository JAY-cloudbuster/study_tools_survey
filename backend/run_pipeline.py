import os
import sys
import time
import psycopg2
from dotenv import load_dotenv
from pipeline.orchestrator import PipelineOrchestrator
from pipeline.pipeline_logger import logger

load_dotenv()


def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def log_pipeline_start():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO pipeline_runs (pipeline_name, run_start, status)
        VALUES (%s, NOW(), %s)
        RETURNING run_id
        """,
        ("study_analytics_pipeline", "RUNNING")
    )

    run_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return run_id


def log_pipeline_end(run_id, status):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE pipeline_runs
        SET run_end = NOW(),
            status = %s
        WHERE run_id = %s
        """,
        (status, run_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def main():

    logger.info("Initializing Study Analytics Pipeline")

    run_id = log_pipeline_start()

    pipeline = PipelineOrchestrator()

    try:

        pipeline.add_step(
            "Baseline Cohort ETL",
            ["etl/baseline_etl.py"]
        )

        pipeline.add_step(
            "Weekly Observations ETL",
            ["etl/weekly_etl.py"]
        )

        pipeline.add_step(
            "Student Performance Loader",
            ["etl/student_performance_loader.py"]
        )

        pipeline.add_step(
            "Stress Dataset Loader",
            ["etl/stress_loader.py"]
        )

        pipeline.add_step(
            "Refresh Analytics Views",
            [
                r"C:\Program Files\PostgreSQL\18\bin\psql.exe",
                "-U",
                os.getenv("DB_USER"),
                "-d",
                os.getenv("DB_NAME"),
                "-f",
                "sql/refresh_views.sql"
            ]
        )

        pipeline.run()

        log_pipeline_end(run_id, "SUCCESS")

        logger.info("Pipeline execution finished successfully")

    except Exception as e:

        log_pipeline_end(run_id, "FAILED")

        logger.error(f"Pipeline failed: {str(e)}")

        raise


if __name__ == "__main__":
    main()