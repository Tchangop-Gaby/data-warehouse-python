import pandas as pd
from sqlalchemy.engine import Engine


COLUMNS = {
    "dim_customer": [
        "customer_key",
        "customer_id",
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
        "product_id",
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
    "fact_sales": [
        "sales_key",
        "sales_number",
        "customer_key",
        "product_key",
        "order_date_key",
        "ship_date_key",
        "due_date_key",
        "quantity",
        "unit_price",
        "sales_amount",
    ],
}

def load_customer_dimension(
        dataframe: pd.DataFrame,
        table_name: str,
        columns: list[str],
        engine: Engine,
) -> None:

    dataframe = dataframe[columns]

    dataframe.to_sql(
        table_name,
        engine,
        schema="warehouse",
        if_exists="append",
        index=False,
    )