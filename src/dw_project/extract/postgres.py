"""
Staging Table Reader
====================

Purpose:
    Read data from staging tables into pandas DataFrames.

Description:
    Provides a controlled way to retrieve data from the
    staging schema while restricting access to known
    staging tables.

Components:
    ALLOWED_STAGING_TABLES:
        Defines the staging tables that can be read.
    read_staging_table():
        Reads all records from a staging table.
"""
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

# Restrict database queries to known staging tables
ALLOWED_STAGING_TABLES = {
    "crm_cust_info",
    "crm_prd_info",
    "crm_sales_details",
    "erp_cust_az12",
    "erp_loc_a101",
    "erp_px_cat_g1v2",
}

def read_staging_table(
        table_name: str,
        engine: Engine,
) -> pd.DataFrame:
    """
    Read all records from a staging table.

    Args:
        table_name:
            Name of the staging table to read.
        engine:
            SQLAlchemy database engine.

    Returns:
        DataFrame containing all records from staging table.
    
    Raises:
        ValueError:
            If the table is not an allowed staging table.
    """
    if table_name not in ALLOWED_STAGING_TABLES:
        raise ValueError(f"Invalid staging table: {table_name}")

    query = text(f"SELECT * FROM staging.{table_name}")

    return pd.read_sql(query, engine)