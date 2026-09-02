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
        "cst_key": ["AW00011000"],
        "cst_firstname": [" Jon"],
        "cst_lastname": ["Yang "],
        "cst_marital_status": ["M"],
        "cst_gndr": ["M"],
        "cst_create_date": ["2025-10-06"],
    })

    cust_az12 = pd.DataFrame({
        "CID": ["NASAW00011000"],
        "BDATE": ["1971-10-06"],
        "GEN": ["Male"],
    })

    loc_a101 = pd.DataFrame({
        "CID": ["AW-00011000"],
        "CNTRY": ["DE"],
    })

    result = transform_customer(
        cust_info,
        cust_az12,
        loc_a101,
    )

    assert len(result) == 1
    assert result.iloc[0]["customer_id"] == 1
    assert result.iloc[0]["first_name"] == "Jon"
    assert result.iloc[0]["country"] == "Germany"
    assert result.iloc[0]["birth_date"] == pd.Timestamp('1971-10-6')

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