"""
Warehouse Table Reader
======================

Purpose:    
    Read data from warehouse dimension tables 
    into pandas DataFrame.

Description:
    Provides controlled access to approved warehouse 
    tables while preventing queries against tables 
    outside the suported dimension set.

Compononts:
    read_warehouse_table():
        Read all records from an approved warehouse table.
"""
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine


def read_warehouse_table(
        table_name: str,
        engine: Engine,
) -> pd.DataFrame:
    """
    Read all records from an approved 
    warehouse dimension table.
    """
    allowed_tables = {
        "dim_customer",
        "dim_product",
        "dim_date",
    }

    # Restrict warehouse queries to known dimension tables.
    if table_name not in allowed_tables:
        raise ValueError(f"Invalid warehouse table: {table_name}")

    query = text(f"SELECT * FROM warehouse.{table_name}")

    return pd.read_sql(query, engine)