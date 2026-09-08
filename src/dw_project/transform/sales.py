"""
Sales Data Transformation
=========================

Purpose:
    Clean, standardize, and prepare sales transaction data for
    the sales fact table.

Description:
    Transforms sales transaction data by standardizing columns,
    converting data fields, reconciling sales amounts and
    unit prices, and renaming source fields to the final data
    warehouse naming convention.

Components:
    reconcile_sales_total():
        Reconciles sales amounts and unit prices
    transform_sales():
        Executes the complete sales transformation.
"""
import pandas as pd

from .common import (
    standardize_columns,
    convert_dates,
)

def reconcile_sales_total(sales_details: pd.DataFrame) -> pd.DataFrame:
    """
    Recincile sales amounts and unit prices in sales trasnformations,

    Whent the unit price is zero but quantity is available, the unit price
    is calculated from the sales amount and quantity. Negative prices and
    sales values are converted to positive values and the sales amount is
    recalculated from unit prices and quantiy

    Args:
        sales_details: Sales transaction DataFrame.
    
    Returns:
        DataFrame containing reconciled sales values.
    """
    sales = sales_details.copy()
    
    sales["sls_price"] = sales["sls_price"].abs()
    sales["sls_quantity"] = sales["sls_quantity"].abs()
    sales["sls_sales"] = sales["sls_sales"].abs()

    mask = (
        (sales["sls_price"] == 0) &
        (sales["sls_quantity"] != 0)
    )

    # Derive missing unit prices from the recorded sales amount.
    sales.loc[mask, "sls_price"] = (
        sales.loc[mask, "sls_sales"] /
        sales.loc[mask, "sls_quantity"]
    )

    # Ensure the sales amount is consistent with price and quantity
    sales["sls_sales"] = (
        sales["sls_price"] * sales["sls_quantity"]
    )

    return sales    

def transform_sales(
        sales_details: pd.DataFrame
) -> pd.DataFrame:
    """
    Transform sales transaction data into the final fact structure.

    The transformation standardizes column names, removes records
    without an order number, converts date fields, reconciles 
    sales values, and renames the source fields to the final 
    warehouse schema.

    Args:   
        sales_details:
            Raw sales transaction DataFrame.

    Returns:
        DataFrame containing the transformed sales transactions.
    """
    sales = standardize_columns(sales_details).copy()

    # Records without an order number cannot be identified as transactions
    sales = sales.dropna(subset=["sls_ord_num"])

    sales["sls_order_dt"] = convert_dates(sales["sls_order_dt"])
    sales["sls_ship_dt"] = convert_dates(sales["sls_ship_dt"])
    sales["sls_due_dt"] = convert_dates(sales["sls_due_dt"])

    sales = reconcile_sales_total(sales)

    # Rename source fields to the final fact table naming convention.
    result = sales.rename(
        columns={
            "sls_ord_num": "order_number",
            "sls_prd_key": "product_key_source",
            "sls_cust_id": "customer_id_source",
            "sls_order_dt": "order_date",
            "sls_ship_dt": "ship_date",
            "sls_due_dt": "due_date",
            "sls_sales": "sales_amount",
            "sls_quantity": "quantity",
            "sls_price": "unit_price",
        }
    )

    return result[
        [
            "order_number",
            "product_key_source",
            "customer_id_source",
            "order_date",
            "ship_date",
            "due_date",
            "sales_amount",
            "quantity",
            "unit_price",
        ]
    ]

def resolve_customer_keys(
        sales_df: pd.DataFrame,
        customer_dim: pd.DataFrame,
) -> pd.DataFrame:
    """
    Resolve source customer IDs to warehouse
    customer surrogate keys.
    """
    lookup = customer_dim[
        [
            "customer_key",
            "customer_id",
        ]
    ].copy()

    result = sales_df.merge(
        lookup,
        how="left",
        left_on="customer_id",
        right_on="customer_id",
        validate="many_to_one",
    )

    result = result.drop(
        columns=["customer_id"]
    )

    return result

def resolve_product_keys(
        sales_df: pd.DataFrame,
        product_dim: pd.DataFrame,
) -> pd.DataFrame:
    """
    Resolve source product IDs to warehouse
    customer surrogate keys.
    """
    lookup = product_dim[
        [
            "product_key",
            "product_code",
        ]
    ].copy()

    result = sales_df.merge(
        lookup,
        how="left",
        on="product_code",
        validate="many_to_one",
    )

    return result

def resolve_date_key(
        sales_df: pd.DataFrame,
        date_dim: pd.DataFrame,
        source_column: str,
        target_column: str,
) -> pd.DataFrame:
    """
    Resolve source date IDs to warehouse
    customer surrogate keys.
    """
    lookup = date_dim[
        [
            "date_key",
            "full_date",
        ]
    ].copy()

    result = sales_df.merge(
        lookup,
        how="left",
        left_on=source_column,
        right_on="full_date",
        validate="many_to_one",
    )

    result = result.rename(
        columns={
            "date_key": target_column
        }
    )

    result = result.drop(
        columns=["full_date"]
    )

    return result 

def prepare_fact_sales(
        sales_df: pd.DataFrame,
        customer_dim: pd.DataFrame,
        product_dim: pd.DataFrame,
        date_dim: pd.DataFrame,
) -> pd.DataFrame:
    """
    Resolve dimension and date keys and 
    prepare sales fact records.
    """
    result = sales_df.copy()

    result = resolve_customer_keys(
        result,
        customer_dim,
    )

    result = resolve_product_keys(
        result,
        product_dim,
    )

    result = resolve_date_key(
        result,
        date_dim,
        "order_date",
        "order_date_key",
    )

    result = resolve_date_key(
        result,
        date_dim,
        "ship_date",
        "ship_date_key",
    )

    result = resolve_date_key(
        result,
        date_dim,
        "due_date",
        "due_date_key",
    )

    result["customer_key"] = (
        result["customer_key"]
        .fillna(0)
        .astype(int)
    )

    result["product_key"] = (
        result["product_key"]
        .fillna(0)
        .astype(int)
    )

    result["order_date_key"] = (
        result["order_date_key"]
        .fillna(0)
        .astype(int)
    )

    result["ship_date_key"] = (
        result["ship_date_key"]
        .fillna(0)
        .astype(int)
    )

    result["due_date_key"] = (
        result["due_date_key"]
        .fillna(0)
        .astype(int)
    )

    return result    