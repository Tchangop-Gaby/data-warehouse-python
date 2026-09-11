"""
Logging Configuration
=====================

Purpose:
    Configure application logging for the 
    ETL pipeline.

Description:
    Creates the log directory and configure 
    logging to wirte message to both the 
    pipeline log file and the console using a 
    consistent format.

Compononts:
    configure_logging():
        Initializes the pieline logging configuration.
"""
import logging
from pathlib import Path


def configure_logging():
    """
    Configure logging to wirte to both 
    the pipeline log and console.
    """
    Path("logs").mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(
                "logs/pipeline.log",
                mode="w"
            ),
            logging.StreamHandler(),
        ],
    )