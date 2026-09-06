"""
Common Data Transformation Utilities
====================================

Purpose:
    Provide reusable validation, column standaardization,
    date conversion, and data cleaning utilities for the 
    transformation layer.

Description:
    This module contains shared functions used across 
    dataset-specific transformations to ensure consistent 
    data quality and formatting.

Component:
    validate_unique_key():
        Checks for duplicate key values.
    standardize_columns():
        Converts column names to lowercase.
    convert_dates():
        Converts values to datetime.
    standardize_date():
        Removes leading and trailing whitespace.
    add_customer_surrogate_key():
        Adds sequentials customer keys.
"""
import pandas as pd

def validate_unique_key(
        dataframe: pd.DataFrame,
        key_column: str,
        dataset_name: str,
) -> None:
    """
    Validates that a dataset contains no duplicate key values.

    Args:
        dataframe: 
            DatFrame containing the key to validate.
        key_column:
            Name of the column that must contain unique values.
        dataset_name:
            Name of the dataset used in the error message.

    Raises:
        ValueError: If duplicate key values are found.
    """
    duplicate_mask = dataframe[key_column].duplicated(keep=False)

    if duplicate_mask.any():
        duplicates = (
            dataframe.loc[duplicate_mask, key_column].dropna().unique()
        )

        raise ValueError(
            f"{dataset_name} contains duplicate "
            f"{key_column} values: {duplicates[:10]}"
        )

def standardize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all DataFrame column names to lowercase.

    Args:
        dataframe:
            DataFrame whose column names should be standardized.
    
    Returns:
        A copy of the DatFrame with lowercase column names.
    """
    dataframe = dataframe.copy()

    dataframe.columns = [
        column.lower()
        for column in dataframe.columns
    ]

    return dataframe

def convert_dates(values: pd.Series) -> pd.Series:
    """
    Convert values to datetime, replacing invalid values 
    with NaT.

    Args:
        values: 
            Series containing date values.
    """
    values = pd.to_datetime(
        values,
        errors="coerce",
    )

    return values

def standardize_data(values: pd.Series) -> pd.Series:
    """
    Remove leading and trailing whitespace from text 
    values.

    Args:
        values:
            Series containing text values.
    
    Return:
        Series containing trimmed text values.
    """
    values = values.str.strip()

    return values

def add_surrogate_key(
        dataframe: pd.DataFrame,
        key_name: str,
) -> pd.DataFrame:
    """
    Add a sequential surrogate key to the customer 
    DataFrame.
    """
    dataframe = dataframe.copy()

    dataframe = dataframe.sort_values(
        by=key_name
    ).reset_index(drop=True)

    dataframe.insert(
        0,
        "customer_key",
        range(1, len(dataframe) + 1),
    )

    return dataframe