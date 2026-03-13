from pipeline.orchestrator import PipelineOrchestrator


def main():

    pipeline = PipelineOrchestrator()

    pipeline.add_step(
        "Baseline ETL",
        ["python", "etl/baseline_etl.py"]
    )

    pipeline.add_step(
        "Weekly Observations ETL",
        ["python", "etl/weekly_etl.py"]
    )

    pipeline.add_step(
        "Student Performance Loader",
        ["python", "etl/student_performance_loader.py"]
    )

    pipeline.add_step(
        "Stress Dataset Loader",
        ["python", "etl/stress_loader.py"]
    )

    pipeline.run()


if __name__ == "__main__":
    main()