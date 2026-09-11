import logging
from pathlib import Path

Path("logs").parent.mkdir(parents=True, exist_ok=True)

def _create_logger(name: str, log_file: str, level: int = logging.INFO,
                    formatter: logging.Formatter | None = None) -> logging.Logger:
    
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if imported muultiple times
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    if formatter is None:
        formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    # Create a handler that writes to a file
    file_handler = logging.FileHandler(Path("logs", log_file), mode='w')

    # Every message follow the defined logging format
    file_handler.setFormatter(formatter)

    # Print logs to the terminal while the program runs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers as destinations for the logs
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