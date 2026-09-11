"""
Logging Configuration
=====================

Purpose:
    Configure dedicated loggers for pipeline, quality, 
    and summary messages.

Description:
    Create the log directory and provides a reusable logger 
    factory that writes messages to both dedicated log files 
    and the console.

Componnents:
    _create_logger():
        Creates and configure a named logger.
    pipeline_logger:
        Logs general pipeline execution messages.
    quality_logger:
        Logs data quality messages.
    summary_logger:
    Logs pipeline summary information.
"""
import logging
from pathlib import Path

# Ensure the log directory exists before creating file handlers
Path("logs").parent.mkdir(parents=True, exist_ok=True)

def _create_logger(name: str, log_file: str, level: int = logging.INFO,
                    formatter: logging.Formatter | None = None) -> logging.Logger:
    """
    Creates and configure a logger with file and 
    console handlers.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers when the module is initialized again
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    if formatter is None:
        formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(Path("logs", log_file), mode='w')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

pipeline_logger = _create_logger(
    "pipeline",
    "pipeline.log",
)
quality_logger = _create_logger(
    "quality",
    "quality.log",
)
summary_logger = _create_logger(
    "summary",
    "summary.log",
    formatter=logging.Formatter("%(asctime)s | %(message)s"),
)