import subprocess
import time
import sys
from pipeline.pipeline_logger import logger


class PipelineOrchestrator:

    def __init__(self):
        self.steps = []

    def add_step(self, name, command):
        self.steps.append((name, command))

    def run(self):

        logger.info("Pipeline execution started")

        for name, command in self.steps:

            start = time.time()
            logger.info(f"Starting step: {name}")

            try:

                # If step is a Python script
                if command[0].endswith(".py"):
                    subprocess.run([sys.executable] + command, check=True)

                # Otherwise run system command directly
                else:
                    subprocess.run(command, check=True)

                duration = time.time() - start
                logger.info(f"{name} completed in {duration:.2f}s")

            except subprocess.CalledProcessError:

                logger.error(f"{name} FAILED")
                raise

        logger.info("Pipeline execution completed")