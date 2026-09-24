"""
Warehouse Table Loader
======================

Purpose:
    Load transformed datasets into warehouse 
    tables.

Description:
    Define the expected column structure for
    warehouse tables and provides a reusable
    function for selecting the required 
    columns and appending transformed data to 
    the warehouse schema.

Components:
    COLUMNS: 
        Defines the expected columns for each warehouse table.
    load_dimension():
        Loads a DataFrame into a warehouse table.
"""
import pandas as pd
from sqlalchemy.engine import Engine


COLUMNS = {
    "dim_customer": [
        "customer_key",
        "customer_code",
        "first_name",
        "last_name",
        "birth_date",
        "gender",
        "marital_status",
        "country",
        "create_date",
    ],
    "dim_product": [
        "product_key",
        "product_code",
        "product_name",
        "product_cost",
        "product_line",
        "category",
        "subcategory",
        "maintenance",
        "start_date",
        "end_date",
    ],
    "dim_date": [
        "date_key",
        "full_date",
        "day_of_month",
        "day_of_week",
        "day_name",
        "month_number",
        "month_name",
        "quarter_number",
        "year_number",
        "week_number",
    ],
}

def load_dimension(
        dataframe: pd.DataFrame,
        table_name: str,
        columns: list[str],
        engine: Engine,
) -> None:
    """
    Append selected DataFrame columns to a
    warehouse table.
    """

    # Select only the columns required by the target warehouse table.
    dataframe = dataframe[columns]

    dataframe.to_sql(
        table_name,
        engine,
        schema="warehouse",
        if_exists="delete_rows",
        index=False,
    )