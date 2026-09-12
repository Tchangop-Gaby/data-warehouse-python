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
    check_non_negative,
    check_referential_integrity,
    check_row_count_reconciliation,
    check_date_sequence,
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

def test_sales_cannot_be_negative():
    """
    Verify that negative sales amounts fail 
    the non-negative check.
    """
    df = pd.DataFrame({
        "sales_amount": [100, 200, -50]
    })

    result = check_non_negative(
        df,
        "sales_amount",
        "sales_amount_non_negative",
    )

    assert result.status == QualityStatus.FAIL

def test_referential_integrity_fails():
    """
    Verify that invalid foreign keys cause 
    referential integrity to fail.
    """
    fact = pd.DataFrame({
        "customer_key": [1, 2 , 99]
    })

    customer_dim = pd.DataFrame({
        "customer_key": [0, 1, 2]
    })

    result = check_referential_integrity(
        fact,
        "customer_key",
        customer_dim,
        "customer_key",
        "fact_customer_fk_valid",
    )

    assert result.status == QualityStatus.FAIL

def test_row_count_reconciliation_passes():
    """
    Verify that matching source and target row 
    counts pass validation
    """
    source = pd.DataFrame({
        "id": [1, 2, 3]
    })

    target = pd.DataFrame({
        "id": [10, 20, 30]
    })

    result = check_row_count_reconciliation(
        source,
        target,
        "sales_to_fact_row_count",
    )

    assert result.status == QualityStatus.PASS

def test_row_count_reconciliation_fails():
    """
    Verify that different source and target row 
    counts fail validation
    """
    source = pd.DataFrame({
        "id": [1, 2, 3]
    })

    target = pd.DataFrame({
        "id": [10, 20]
    })

    result = check_row_count_reconciliation(
        source,
        target,
        "sales_to_fact_row_count",
    )

    assert result.status == QualityStatus.FAIL

def test_sales_date_sequence():
    """
    Verify that order, ship, and due date follows 
    correct sequence
    """
    df = pd.DataFrame({
        "order_date": [pd.Timestamp("2024-01-01")],
        "ship_date": [pd.Timestamp("2024-01-03")],
        "due_date": [pd.Timestamp("2024-01-05")],
    })

    order_and_ship_result = check_date_sequence(
        df,
        "order_date",
        "ship_date",
        "order_and_ship_date_sequence_valid"
    )

    ship_and_due_result = check_date_sequence(
        df,
        "ship_date",
        "due_date",
        "ship_and_due_date_sequence_valid"
    )

    assert order_and_ship_result.status == QualityStatus.PASS
    assert ship_and_due_result.status == QualityStatus.PASS