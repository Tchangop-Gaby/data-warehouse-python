"""
Data Quality Check Tests
========================

Purpose:
    Verify the behavior of common data quality 
    validation rules.

Description:
    Tests successful and failed not-null checks
    and verifies that duplicate values are correctly
    detected by the uniqueness check.

    Tests:
        test_not_null_passes():
            Verifies that a column without null values passes.
        test_not_null_fails():
            Verifies that null values cause a check fail.
        test_unique_fails():
            Verifies that duplicate values cause a check to fail.
"""
import pandas as pd

from dw_project.quality.checks import (
    check_not_null,
    check_unique,
)
from dw_project.quality.result import QualityStatus


def test_not_null_passes():
    """
    Verify that a column without null values
    passes the not-null check.
    """
    df = pd.DataFrame({
        "customer_id": [1, 2, 3]
    })

    result = check_not_null(
        df,
        "customer_id",
        "customer_id_not_null",
    )

    assert result.status == QualityStatus.PASS
    assert result.rows_affected == 0

def test_not_null_fails():
    """
    Verify that a column containing null values 
    fails the not-null check.
    """
    df = pd.DataFrame({
        "customer_id": [1, None, 3]
    })

    result = check_not_null(
        df,
        "customer_id",
        "customer_id_not_null",
    )

    assert result.status == QualityStatus.FAIL
    assert result.rows_affected == 1

def test_unique_fails():
    """
    Verify that duplicate values fail the uniqueness 
    check.
    """
    df = pd.DataFrame({
        "customer_id": [1, 2, 2, 3]
    })

    result = check_unique(
        df,
        "customer_id",
        "customer_id_unique",
    )

    assert result.status == QualityStatus.FAIL
    assert result.rows_affected == 2