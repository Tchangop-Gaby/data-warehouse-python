"""
Customer Transformation Tests
=============================

Purpose:
    Verify the customer transformation and validation logic.

Description:
    Tests successful customer data transformation and verifies 
    that duplicate auxiliary customer keys are rejected.

Tests:
    test_customer_transform():
        Verifies successful customer transformation.
    test_customer_duplicate_auxiliary_key():
        Verifies duplicate aixiliary keys raise a validation error.
"""
import pandas as pd
import pytest

from dw_project.transform.customer import (
    transform_customer,
)

def test_customer_transform():
    """
    Verify that customer data is transformed
    and merged correctly
    """
    cust_info = pd.DataFrame({
        "cst_id": [1],
        "cst_key": ["C001"],
        "cst_firstname": ["John"],
        "cst_lastname": ["Doe"],
        "cst_marital_status": ["M"],
        "cst_gndr": ["M"],
        "cst_create_date": ["2024-01-01"],
    })

    cust_az12 = pd.DataFrame({
        "CID": ["C001"],
        "BDATE": ["1990-05-10"],
        "GEN": ["M"],
    })

    loc_a101 = pd.DataFrame({
        "CID": ["C001"],
        "CNTRY": ["USA"],
    })

    result = transform_customer(
        cust_info,
        cust_az12,
        loc_a101,
    )

    assert len(result) == 1
    assert result.iloc[0]["customer_id"] == 1
    assert result.iloc[0]["first_name"] == "John"
    assert result.iloc[0]["country"] == "United States"

def test_customer_duplicate_auxiliary_key():
    """
    Verify that duplicate auxiliary customer keys
    raise ValueError.
    """
    cust_info = pd.DataFrame({
        "cst_id": [1],
        "cst_key": ["C001"],
        "cst_firstname": ["John"],
        "cst_lastname": ["Doe"],
        "cst_marital_status": ["M"],
        "cst_gndr": ["M"],
        "cst_create_date": ["2024-01-01"],
    })

    cust_az12 = pd.DataFrame({
        "CID": ["C001", "C001"],
        "BDATE": ["1990-05-10", "1990-05-10"],
        "GEN": ["M", "M"],
    })

    loc_a101 = pd.DataFrame({
        "CID": ["C001"],
        "CNTRY": ["USA"],
    })


    with pytest.raises(ValueError):
        transform_customer(
            cust_info,
            cust_az12,
            loc_a101,
        )