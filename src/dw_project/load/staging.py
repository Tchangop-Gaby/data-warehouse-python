from dw_project import database
import pandas as pd

def load_to_staging(
        df: pd.DataFrame,
        table_name: str,
        engine: object,
        replace=False
):
    mode = "replace" if replace else "append"

    df.to_sql(
        table_name,
        engine,
        schema="staging",
        if_exists=mode, 
        index=False,
    )