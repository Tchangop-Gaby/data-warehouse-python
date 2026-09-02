"""
Product Transformation Tests
============================

Purpose:
    Verify that product and category data are transformed 
    and combined correctly.

Description:
    Tests the successful transformation of product information
    and its associated category data into the final product 
    dimension structure.

Tests:
    test_product_transform():
        Verifies successful product transformation and category
        enrichment
"""
import pandas as pd

from dw_project.transform.product import (
    transform_product,
)

def test_product_transform():
    """
    Verify that product data is transformed and enriched 
    with category data.
    """
    prd_info = pd.DataFrame({
        "prd_id": [210],
        "prd_key": ["AC-BR-FR-R92B-58"],
        "prd_nm": ["HL Road Frame - Black- 58"],
        "prd_cost": [12.00],
        "prd_line": ["R"],
        "prd_start_dt": ["2003-07-01"],
        "prd_end_dt": ["2007-12-28"],
    })

    cateogry = pd.DataFrame({
        "ID": ["AC_BR"],
        "CAT": ["Accessories"],
        "SUBCAT": ["Bike Racks"],
        "MAINTENANCE": ["Yes"],
    })

    result = transform_product(
        prd_info,
        cateogry,
    )

    assert len(result) == 1
    assert result.iloc[0]["product_key"] == "FR-R92B-58"
    assert result.iloc[0]["category_key"] == "AC_BR"
    assert result.iloc[0]["product_line"] == "Road"
    assert result.iloc[0]["category"] == "Accessories"