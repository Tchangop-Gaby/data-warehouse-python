import pandas as pd
from dw_project.logger import get_looger

logger = get_looger()

def extract_csv(file_path: str) -> pd.DataFrame:

    """
    Extract data from a CSV file into a pandas Dataframe.

    Reads the CSV file specified by 'file_path', logs the
    extraction process and number of rows extracted, and 
    returns the resulting Dataframe.    

    Args:
        file_path(str): Path to the CSV file to be read.

    Returns:
        pd.Dataframe: Data extracted from CSV file.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        Exception: If an unexpected error occurs while reading the file
    """
    try:

        logger.info(f"Reading {file_path}")

        df = pd.read_csv(file_path)

        logger.info(f"Extracted {len(df)} rows from {file_path}")
        
        return df
    
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise

    except Exception:
        logger.exception(f"Failed to read {file_path}")
        raise