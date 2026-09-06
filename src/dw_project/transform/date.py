"""
Date Dimension
==============

Purpose:
    Build a date dimension from the dates used 
    in sales transaction.

Description:
    Extracts unique order, ship, and due dates
    from the sales dataset and derives calendar
    attributes such as year, quarter, month,
    weekday, and week of year for use in the
    data warehouse.

Components:
    create_date_dimension():
        Creates the date dimension DataFrame.
"""
import pandas as pd

def create_date_dimension(
        sales_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a data dimension from order, ship,
    and due dates.
    """

    # Combine all relevant sales dates into a single unique date set.
    dates = pd.concat(
        [
            sales_df["order_date"],
            sales_df["ship_date"],
            sales_df["due_date"],
        ]
    ).dropna().drop_duplicates()

    # Sort dates to produce a consistent dimension order.
    dates = pd.DataFrame({
        "full_date": pd.to_datetime(dates)
    })

    dates = dates.sort_values(
        "full_date"
    ).reset_index(drop=True)

    dates["date_key"] = dates[
        "full_date"
    ].dt.strftime("%Y%m%d").astype(int)

    dates["day_of_month"] = dates[
        "full_date"
    ].dt.day

    dates["day_of_week"] = dates[
        "full_date",
    ].dt.dayofweek + 1

    dates["day_name"] = dates[
        "full_date"
    ].dt.day_name()

    dates["month_number"] = dates[
        "full_date"
    ].dt.month

    dates["month_name"] = dates[
        "full_date"
    ].dt.month_name()

    dates["quarter_number"] = dates[
        "full_date"
    ].dt.quarter

    dates["year_number"] = dates[
        "full_date"
    ].dt.year

    dates["week_number"] = dates[
        "full_date"
    ].dt.isocalendar().week.astype(int)

    return dates[
        [
            "date_key",
            "full_date",
            "day_of_month",
            "day_of_week",
            "day_name",
            "month_number",
            "month_name",
            "quarter_number",
            "year_number",
            "week_number",
        ]
    ]