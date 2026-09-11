"""
Data Quality Rules
==================

Purpose:
    Provide reusable validation rules for checking
    data quality across transformed datasets

Description:
    This module contains common data quality checks for
    nill values, uniqueness, numeric ranges, dates, allowed
    values, referential integrity, sales reconciliation,
    and date sequences.

Components: 
    check_not_null():
        Check for missing values.
    check_unique():
        Checks for duplicate values.
    check_non_negative():
        Checks for negative numeric values.
    check_valid_dates():
        Checks for missing or invalid dates.
    check_allowed_values():
        Checks values against an allowed set.
    check_referential_integrity():
        Validate child-to-parent key relationships.
    check_sales_reconciliation():
        Validates sales amount calculations
    check_product_date_sequence():
        Validates product date ranges.
    check_sales_date_sequence():
        Validates sales date chronology.
"""
import pandas as pd

from .result import (
    QualityStatus,
    QualityResult,
)
from .runner import (
    run_pipeline_checks,
)

def check_not_null(
        dataframe: pd.DataFrame,
        column: str,
        rule_name: str,
) ->QualityResult:
    """
    Check whether a column contains null values.
    """
    null_mask = dataframe[column].isna()

    affected = int(null_mask.sum())
    total = len(dataframe)

    if affected == 0:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=total,
            rows_affected=0,
            message=f"{column} contains no null values",
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{column} contains {affected} null values"
        ),
    )

def check_unique(
        dataframe: pd.DataFrame,
        column: str,
        rule_name: str,
) -> QualityResult:
    """
    Check whether all values in a column are unique.
    """
    duplicate_mask = dataframe[column].duplicated(keep=False)

    affected = int(duplicate_mask.sum())
    total = len(dataframe)

    if affected == 0:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=total,
            rows_affected=0,
            message=f"{column} is unique",
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{column} contains duplicate values"
        ),
    )

def check_non_negative(
        dataframe: pd.DataFrame,
        column: str,
        rule_name: str,
) -> QualityResult:
    """
    Check whether a numeric column contains negative values.
    """
    invalid_mask = dataframe[column].notna() & (
        dataframe[column] < 0
    )

    affected = int(invalid_mask.sum())
    total = len(dataframe)

    if affected == 0:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=total,
            rows_affected=0,
            message=f"{column} contains no negative values",
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{column} contains {affected} "
            "negative values"
        ),
    )

def check_valid_dates(
        dataframe: pd.DataFrame,
        column: str,
        rule_name: str,
) -> QualityResult:
    """
    Check whether a date column contains missing or invalid dates.
    """
    invalid_mask = dataframe[column].isna()

    affected = int(invalid_mask.sum())
    total = len(dataframe)

    if affected == 0:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=total,
            affected=0,
            message=f"{column} contains valid dates"
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{column} contains {affected} "
            "missing or invalid dates"
        ),
    )

def check_allowed_values(
        dataframe: pd.DataFrame,
        column: str,
        allowed_values: set,
        rule_name: str,
) -> QualityResult:
    """
    Check whether non-null values belong to an allowed set.
    """
    invalid_mask = (
        dataframe[column].notna() &
        ~dataframe[column].isin(allowed_values)
    )

    affected = int(invalid_mask.sum())
    total = len(dataframe)

    if affected == 0:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=total,
            rows_affected=0,
            message=f"{column} contains only allowed values"
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{column} contains {affected} "
            "invalid values"
        ),                                
    )

def check_referential_integrity(
        child_df: pd.DataFrame,
        child_column:str,
        parent_df: pd.DataFrame,
        parent_column: str,
        rule_name: str,
) -> QualityResult:
    """
    Check that child keys exist in the corresponding parent dataset.
    """
    valid_keys = set(
        parent_df[parent_column].dropna().unique()
    )

    invalid_mask = (
        child_df[child_column].notna() &
        ~child_df[child_column].isin(valid_keys)
    )

    affected = int(invalid_mask.sum())
    total = len(child_df)

    if affected == 0:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=total,
            rows_affected=0,
            message=(
                f"All {child_column} values "
                "exist in the parent"
            ),
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{affected} {child_column} values "
            "do not exist in the parent"
        ),
    )

def check_sales_reconciliation(
        dataframe: pd.DataFrame,
        tolerance: float = 0.01,
) -> QualityResult:
    """
    Check that sales amount equals quantity multiplied by unit price.
    """
    expected_sales = (
        dataframe["quantity"] * dataframe["unit_price"]
    )

    difference = (
        dataframe["sales_amount"] - expected_sales
    ).abs()

    invalid_mask = difference > tolerance

    affected = int(invalid_mask.sum())
    total = len(dataframe)

    if affected == 0:
        return QualityResult(
            rule_name="sales_reconciliation",
            status=QualityStatus.PASS,
            rows_checked=total,
            rows_affected=0,
            message=(
                "Sales amount reconciles with "
                "quantity * unit price"
            ),
        )

    return QualityResult(
        rule_name="sales_reconciliation",
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{affected} rows failed sales "
            "amount reconciliation"
        )
    )

def check_date_sequence(
        dataframe: pd.DataFrame,
        previous: str,
        next: str,
        rule_name: str,
) -> QualityResult:
    """
    Check that product start dates do not occur after end dates.
    """
    invalid_mask = (
        dataframe[previous] > dataframe[next]
    )

    affected = int(invalid_mask.sum())
    total = len(dataframe)

    if affected == 0:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=total,
            rows_affected=0,
            message=(
                "Dates follow expected sequence"
            ),
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=total,
        rows_affected=affected,
        message=(
            f"{affected} rows contain invalid date sequences"
        ),
    )

def check_row_count_reconciliation(
        source_df: pd.DataFrame,
        target_df: pd.DataFrame,
        rule_name: str,
) -> QualityResult:
    """
    Verify that source and target datasets 
    contain the same number of rows.
    """
    source_count = len(source_df)
    target_count = len(target_df)

    if source_count == target_count:
        return QualityResult(
            rule_name=rule_name,
            status=QualityStatus.PASS,
            rows_checked=source_count,
            rows_affected=0,
            message=(
                f"Source and target both contain "
                f"{source_count} rows"
            ),
        )

    return QualityResult(
        rule_name=rule_name,
        status=QualityStatus.FAIL,
        rows_checked=source_count,
        rows_affected=abs(
            source_count - target_count
        ),
        message=(
            f"Source={source_count}, "
            f"target={target_count}"
        ),
    )

def validate_customers(customer_df: pd.DataFrame) -> list:

    customer_checks = [
        lambda: check_not_null(
            customer_df,
            "customer_id",
            "customer_id_not_null",
        ),

        lambda: check_not_null(
            customer_df,
            "customer_code",
            "customer_code_not_null",
        ),

        lambda: check_unique(
            customer_df,
            "customer_id",
            "customer_id_unique",
        ),

        lambda: check_unique(
            customer_df,
            "customer_code",
            "customer_code_unique",
        ),

        lambda: check_allowed_values(
            customer_df,
            "gender",
            {"Male", "Female", "Unknown"},
            "customer_gender_valid",
        ),

        lambda: check_allowed_values(
            customer_df,
            "marital_status",
            {"Single", "Married", "Unknown"},
            "customer_marital_status_valid",
        ),
    ]

    results = run_pipeline_checks(customer_checks)

    return results

def validate_products(product_df: pd.DataFrame) -> list:

    product_checks = [
        lambda: check_not_null(
            product_df,
            "product_id",
            "product_id_not_null",
        ),

        lambda: check_not_null(
            product_df,
            "product_code",
            "product_code_not_null",
        ),

        lambda: check_unique(
            product_df,
            "product_id",
            "product_id_unique",
        ),

        lambda: check_unique(
            product_df,
            "product_code",
            "product_code_unique",
        ),

        lambda: check_non_negative(
            product_df,
            "product_cost",
            "product_cost_non_negative",
        ),

        lambda: check_date_sequence(
            product_df,
            "start_date",
            "end_date",
            "product_date_sequence_valid",
        ),
    ]

    results = run_pipeline_checks(product_checks)

    return results

def validate_sales(sales_df: pd.DataFrame) -> list:

    sales_checks = [
        lambda: check_not_null(
            sales_df,
            "order_number",
            "sales_order_number_not_null",
        ),

        lambda: check_not_null(
            sales_df,
            "product_key_source",
            "sales_product_key_source_not_null",
        ),

        lambda: check_not_null(
            sales_df,
            "customer_id_source",
            "sales_customer_id_source_not_null",
        ),

        lambda: check_non_negative(
            sales_df,
            "sales_amount",
            "sales_amount_non_negative",
        ),

        lambda: check_non_negative(
            sales_df,
            "quantity",
            "sales_quantity_non_negative",
        ),

        lambda: check_non_negative(
            sales_df,
            "unit_price",
            "unit_price_non_negative",
        ),

        lambda: check_date_sequence(
            sales_df,
            "order_date",
            "ship_date",
            "order_and_ship_date_sequence_valid",
        ),

        lambda: check_date_sequence(
            sales_df,
            "ship_date",
            "due_date",
            "ship_and_due_date_sequence_valid",
        ),

        lambda: check_sales_reconciliation(
            sales_df
        ),
    ]

    results = run_pipeline_checks(sales_checks)

    return results