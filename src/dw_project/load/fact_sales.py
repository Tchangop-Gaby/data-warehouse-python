"""
Fact Table Loader
======================

Purpose:
    Load transformed dataset into warehouse 
    tables.

Description:
    Define the expected column structure for
    warehouse tables and provides a function
    for selecting the required columns and 
    appending transformed data to the warehouse
    schema.

Components:
    FACT_COLUMNS: 
        Defines the expected columns for the fact table.
    load_tables():
        Loads fact table into the warehouse fact table.
"""
import pandas as pd
from sqlalchemy.engine import Engine

FACT_COLUMNS = [
    "order_number",
    "customer_key",
    "product_key",
    "order_date_key",
    "ship_date_key",
    "due_date_key",
    "quantity",
    "unit_price",
    "sales_amount",
]

def load_fact_sales(
        fact_df: pd.DataFrame,
        engine: Engine,
) -> None:

    fact_df = fact_df[FACT_COLUMNS]

    fact_df.to_sql(
        "fact_sales",
        engine,
        schema="warehouse",
        if_exists="delete_rows",
        index=False,
    )