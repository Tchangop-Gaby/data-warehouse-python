import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

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
    if table_name not in ALLOWED_STAGING_TABLES:
        raise ValueError(f"Invalid staging table: {table_name}")
    
    rows_loaded = len(df)

    df.to_sql(
        name=table_name,
        con=engine,
        schema="staging",
        if_exists="append",
        index=False,
        method="multi"
    )

    return rows_loaded

