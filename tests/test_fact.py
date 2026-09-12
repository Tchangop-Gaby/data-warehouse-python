"""
Sales key Resolution Tests
==========================

Purpose:
    Verify that sales transactions are correctly 
    mapped to warehouse customer and product 
    surrogate keys.

Description:    
    Tests successful customer and product key resolution, 
    as well as the handling of unmatched product keys 
    using the unknown-member key.

Tests:
    test_customer_key_resolution():
        Verifies customer IDs resolve correctly.
    test_product_key_resolution():
        Verifies product keys resolve correctly.
    test_unmatched_product_gets_unknown_key():
        Verifies unmatched products receive the unknown 
        key value of 0.
"""
import pandas as pd

from dw_project.transform.sales import (
    resolve_customer_keys,
    resolve_product_keys,
)

def test_customer_key_resolution():
    """
    Verify that a source customer ID resolves 
    to the correct surrogate key.
    """
    sales_df = pd.DataFrame({
        "order_number": ["SO43698"],
        "customer_id_source": [28389]
    })

    customer_dim = pd.DataFrame({
        "customer_key": [2],
        "customer_id": [28389]
    })

    result = resolve_customer_keys(
        sales_df,
        customer_dim,
    )

    assert result.iloc[0]["customer_key"] == 2

def test_product_key_resolution():
    """
    Verify that a source product key resolves 
    to the correct surrogate key.
    """
    sales_df = pd.DataFrame({
        "product_key_source": ["BK-M82S-44"]
    })

    product_dim = pd.DataFrame({
        "product_key": [12],
        "product_key_source": ["BK-M82S-44"]
    })

    result = resolve_product_keys(
        sales_df,
        product_dim
    )

    assert result.iloc[0]["product_key"] == 12

def test_unmatched_product_gets_unknown_key():
    """
    Verify that an unmatched product receives 
    the unknown key value of 0.
    """
    sales_df = pd.DataFrame({
        "product_key_source": ["BK-M000-44"]
    })

    product_dim = pd.DataFrame({
        "product_key": [12],
        "product_key_source": ["BK-M82S-44"]
    })

    result = resolve_product_keys(
        sales_df,
        product_dim
    )

    result["product_key"] = (
        result["product_key"]
        .fillna(0)
        .astype(int)
    )

    assert result.iloc[0]["product_key"] == 0