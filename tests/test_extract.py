"""
CSV Loader Tests
================

Purpose:
    Verify the CSV extraction and column validation
    functionality.

Description:
    Tests successful CSV loading, handling of missing
    files, and validation of expected DataFrame
    columns.
"""
from pathlib import Path
import pandas as pd
import pytest

from dw_project.extract.csv_loader import (
    load_csv,
    validate_columns,
)

def test_load_csv(tmp_path):
    """
    Verify that a CSV file is loaded with the correct
    metadata and columns.
    """
    file_path = tmp_path / "test.csv"

    dataframe = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["A", "B", "C"],
    })

    dataframe.to_csv(file_path, index=False)

    result = load_csv(file_path)

    assert result.row_count == 3
    assert result.column_count == 2
    assert list(result.dataframe.columns) == [
        "id",
        "name",
    ]

def test_load_csv_missing_file():
    """
    Verify that loading a non-existent file raises
    FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        load_csv(Path("does_not_exists.csv"))

def test_validate_column_success():
    """
    Verify that a DataFrame with the expected column
    passes validation.
    """
    dataframe = pd.DataFrame({
        "id": [1],
        "name": ["A"],
    })

    validate_columns(
        dataframe,
        ["id","name"],
    )

def test_validate_columns_missing_column():
    """
    Verify that a missing expected column raises ValueError.
    """
    dataframe = pd.DataFrame({
        "id": [1],
    })

    with pytest.raises(ValueError):
        validate_columns(
            dataframe,
            ["id","name"], 
        )