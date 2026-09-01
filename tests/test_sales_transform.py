"""
Sales Transformation Tests
==========================

Purpose:
    Verify that sales transaction data is transformed
    correctly.

Description:
    Tests the successful transformation of sales data 
    into the final sales fact table structure, 
    including field renaming and value types

Tests:
    test_sales_transform():
        Verifies successful sales transformation.
"""
import pandas as pd

from dw_project.transform.sales import (
    transform_sales,
)

def test_sales_transform():
    """
    Verify that sales transaction data is transformed 
    correctly
    """
    sales = pd.DataFrame({
        "sls_ord_num": ["SO43697"],
        "sls_prd_key": ["BK-R93R-62"],
        "sls_cust_id": [21768],
        "sls_order_dt": ["20101229"],
        "sls_ship_dt": ["20110105"],
        "sls_due_dt": ["20110110"],
        "sls_sales": [100],
        "sls_quantity": [-2],
        "sls_price": [50],
    })

    result = transform_sales(sales)

    assert len(result) == 1
    assert result.iloc[0]["order_date"] == 2010-12-29
    assert result.iloc[0]["sales_amount"] == 100
    assert result.iloc[0]["quantity"] == 2
    assert result.iloc[0]["unit_price"] == 50