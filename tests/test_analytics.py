"""
Analytics View Tests
====================

Purpose:
    Verify that analytical views produce results 
    consistent with warehouse fact table data.

Description:
    Tests that aggregated sales metrics in the analytics 
    layer reconcile with the corresponding totals in 
    the warehouse fact table.
"""
import pandas as pd
from dw_project.database import create_db_engine

def test_monthly_sales_reconcile_with_fact(test_engine=create_db_engine()):
    """
    Verify that analytics sales totals reconcile 
    with the fact table.
    """
    fact_total = pd.read_sql(
        """
        SELECT SUM(sales_amount) AS total
        FROM warehouse.fact_sales
        """,
        test_engine,
    ).iloc[0]["total"]

    analytics_total = pd.read_sql(
        """
        SELECT SUM(total_sales) AS total
        FROM analytics.sales_summary
        """,
        test_engine,
    ).iloc[0]["total"]

    assert fact_total == analytics_total