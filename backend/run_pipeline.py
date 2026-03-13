from pipeline.orchestrator import PipelineOrchestrator
from pipeline.pipeline_logger import logger


def main():

    logger.info("Initializing Study Analytics Pipeline")

    pipeline = PipelineOrchestrator()

    # -----------------------------
    # ETL STEPS
    # -----------------------------

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

    # -----------------------------
    # RUN PIPELINE
    # -----------------------------

    logger.info("Starting pipeline execution")

    pipeline.run()

    logger.info("Pipeline execution finished successfully")


if __name__ == "__main__":
    main()