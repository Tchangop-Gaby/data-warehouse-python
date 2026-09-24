"""
CSV Extraction and V alidation
==============================

Purpose:
    Load CSV files and validate their structure
    before processing.

Description:
    Provides CSV extraction functionality and validates
    Dataframes columns against an expected schema.

Components:
    ExtracionResult:
        Stores extracted data and dataset metadata.
    load_csv():
        Loads and validates a CSV file.
    validate_columns():
        Validates the DataFrame column structure.
"""
from pathlib import Path
from dataclasses import dataclass
from dw_project.logger_config import pipeline_logger

import pandas as pd

@dataclass
class ExtractionResult:
    """Stores extracted data and basic dataset metadata."""
    file_path: Path
    dataframe: pd.DataFrame
    row_count: int
    column_count: int

def load_csv(file_path: Path) -> ExtractionResult:
    """
    Load a CSV file and return its data with extraction metadata.

    Args:
        file_path: Path to the CSV files.
    
    Returns:
        ExtractionResult containing the file_path, Dataframe, and dimensions.
    
    Raises:
        FileNotFoundError:
            If the source file does not exist.
        ValueError:
            If the file s not a CSV.
    """
    if not file_path.exists():
        pipeline_logger.exception(f"Source file not found: {file_path}")

    if file_path.suffix.lower() != ".csv":
        pipeline_logger.exception(f"Expected a CSV file received: {file_path}")

    df = pd.read_csv(file_path)

    return ExtractionResult(
        file_path=file_path,
        dataframe=df,
        row_count=len(df),
        column_count=len(df.columns),
    )

def validate_columns(df: pd.DataFrame, expected_columns: list[str]) -> None:
        """
        Validate that the DataFrame matches the expected column schema.

        Args:
            dataframe: DataFrame to validate.
            expected_columns: Required column names
        
        Raises:
            ValueError: 
                If column are missing or unexpected columns are presunf.
        """
        actual_columns = list(df.columns)

        missing_columns = [column for column in expected_columns if column not in actual_columns]

        unexpected_columns = [column for column in actual_columns if column not in expected_columns]

        if missing_columns:
            pipeline_logger.exception(f"Missing columns: {missing_columns}")

        if unexpected_columns:
            pipeline_logger.exception(f"Unexpected columns: {unexpected_columns}")