import logging
from pathlib import Path

def get_looger(name: str = "dw_pipeline"):
    """
    Create and configure a logger for the data
    warehouse pipeline.

    The logger writes messages to both the console
    and the 'logs.pipeline.log file. The 'logs  
    directory is created automatically if it does 
    not already exist.

    Args:
        name (str): Name of the logger. Default to "dw_pipeline".

    Returns:
        logging.logger: A configured logger instance.
    """

    Path("logs").mkdir(exist_ok=True)

    handler = logging.FileHandler("logs/pipeline.log")

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | %(levelname)s | %(name)s %(message)s"),
        handlers=[
            handler,
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger(name)