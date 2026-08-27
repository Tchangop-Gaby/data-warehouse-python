"""
Staging Table Loader
====================

Purpose:
    Manage truncation and loading of data into
    staging tables.

Description:
    Provides functions for safely clearing staging
    tables and loading pandas DataFrames into the
    staging schema.

Components:
    ALLOWED_STAGING_TABLES:
        Defines the staging tables that can be modified.
    truncate_staging_table():
        Clears a staging table.
    load_dataframe_to_staging():
        Loads a DataFrame into a staging table.
"""
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

# Restrict database operations to known staging tables.
ALLOWED_STAGING_TABLES = {
    "crm_cust_info",
    "crm_prd_info",
    "crm_sales_details",
    "erp_cust_az12",
    "erp_loc_a101",
    "erp_px_cat_g1v2"
}

def truncate_staging_table(
        table_name: str,
        engine: Engine
) -> None:
    """
    Remove all existing records from a a staging table/

    Args:
        table_name: Name of the staging table to truncate.
        engine: SQLAlchemy database engine.
    
    Raises:
        ValueError: If the table is not an allowed staging table.
    """
    if table_name not in ALLOWED_STAGING_TABLES:
        raise ValueError(f"Invalid staging table: {table_name}")

    query = text(f"TRUNCATE TABLE staging.{table_name}")

    with engine.begin() as connection:
        connection.execute(query)

def load_dataframe_to_staging(
        df: pd.DataFrame,
        table_name: str,
        engine: Engine
) -> int:
    """
    Append DataFrame records to a staging table.

    Args:
        dataframe:
            DataFrame containg the records to load.
        table_name: 
            Name of the target staging table.
        engine:
            SQLAlchemy database engine
    
    Returns:
        Number of rows loaded into the staging table.

    Raises:
        ValueError: If the table is not an allowed staging table.
    """
    if table_name not in ALLOWED_STAGING_TABLES:
        raise ValueError(f"Invalid staging table: {table_name}")
    
    rows_loaded = len(df)

    df.columns = df.columns.str.lower()
  
    df.to_sql(
        name=table_name,
        con=engine,
        schema="staging",
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    return rows_loaded

