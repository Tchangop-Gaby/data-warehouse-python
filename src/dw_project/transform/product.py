"""
Product Data Transformation
===========================

Purpose:
    Clean, standardize, reconcile, and combine product datasets
    into the final product dimension structure.

Description:
    Transform product information and category data by standardizing
    columns, validating keys, deriving category keys, normalizing
    product lines, correcting date chronology, and joining category
    attributes.

Components:
    derive_category_key():
        Extracts product and category keys.
    reconcile_key():
        Aligns category key formats.
    normalize_product_line():
        Standardizes product line values.
    enforce_chronology():
        Ensures product date ranges follow a valid order.
    transform_product():
        Execute the complete product trasnformation.
"""
import pandas as pd

from .common import (
    validate_unique_key,
    standardize_columns,
    convert_dates,
)

def derive_category_key(prd_info: pd.DataFrame) -> pd.DataFrame:
    """
    Derive product and category keys from the source product key.

    Args:
        prd_info:
            Product information DataFrame.
    
    Returns:
        DataFrame containing seperate product and category keys.
    """
    prd_info = prd_info.copy()

    prd_info["cat_key"] = prd_info["prd_key"].str[:5]
    prd_info["prd_key"] = prd_info["prd_key"].str[6:]

    # Place the derived category key next to the product key.
    cat_key = prd_info.pop("cat_key")
    prd_info.insert(2, "cat_key", cat_key)

    return prd_info

def reconcile_key(values: pd.Series) -> pd.Series:
    """
    Standardize category key seperators.

    Args:
        value:
            Series containing category keys.
    
    Returns:
        DataFrame with standardized category keys.
    """

    values = values.str.replace("-", "_", regex=False)

    return values

def normalize_product_line(value: pd.Series) -> pd.Series:
    """
    Convert product line codes to standardizednames.

    Args:
        values:
            Series containing raw product line values.
    
    Returns:    
        Series containing standardized product line names.
    """
    value = value.fillna("").astype(str).str.strip().str.upper()

    return value.map({
        "M": "Mountain",
        "R": "Road",
        "S": "Other Sales",
        "T": "Touring",
    }).fillna("Unknown")

def enforce_chronology(prd_info: pd.DataFrame) -> pd.DataFrame:
    """
    Correct invalid product date ranges using the next start date.

    Products are ordered by the key and start date. When a product's
    end date occurs before or on its start date, the end date is set
    to the day before the next product version starts.

    Args:
        prd_info:
            Product information DataFrame with converted date fields.
    
    Returns:
        DataFrame with corrected products date ranges.
    """
    prd_info = prd_info.copy()

    prd_info = prd_info.sort_values(["prd_key", "prd_start_dt"])

    invalid_dates = prd_info["prd_start_dt"] >= prd_info["prd_end_dt"]

    next_start_date = (
        prd_info.groupby("prd_key")["prd_start_dt"].shift(-1) - pd.Timedelta(days=1)
    )

    # Use the next product version to determine the valid end date.
    prd_info.loc[
        invalid_dates,
        "prd_end_dt",
    ] = next_start_date[invalid_dates]

    return prd_info

def transform_product(
        prd_info: pd.DataFrame,
        px_cat_g1v2: pd.DataFrame,
) -> pd.DataFrame:
    """
    Transform product and category data into the product dimension.

    The trasnformation standardizes source schemas, validates keys,
    derives, and reconcile keys, normalizes product lines and dates,
    corrects date chronology, and joins category information.

    Args:
        prd_info:
            Product information DataFrame
        px_cat_g1v2:
            Product category DataFrame.
    
    Returns:
        DataFrame containing the transformed product dimension data.

    Raises:
        ValueError:
            If duplicate product or category keys are found.
    """
    prd_info = standardize_columns(prd_info).copy()
    px_cat_g1v2 = standardize_columns(px_cat_g1v2).copy()

    # Remove records without the keys required for validation and joins.
    prd_info = prd_info.dropna(subset=["prd_id"])
    prd_info = prd_info.dropna(subset=["prd_key"])
    px_cat_g1v2 = px_cat_g1v2.dropna(subset=["id"])

    prd_info = prd_info.drop_duplicates(subset=["prd_key"], keep="first")

    validate_unique_key(
        prd_info,
        "prd_id",
        "prd_info",
    )

    validate_unique_key(
        px_cat_g1v2,
        "id",
        "px_cat_g1v2",
    )

    prd_info = derive_category_key(prd_info)

    prd_info["cat_key"] = reconcile_key(prd_info["cat_key"])

    prd_info["prd_line"] = normalize_product_line(prd_info["prd_line"])

    prd_info["prd_start_dt"] = convert_dates(prd_info["prd_start_dt"])
    prd_info["prd_end_dt"] = convert_dates(prd_info["prd_end_dt"])

    prd_info = enforce_chronology(prd_info)

    # Category data is many-to-one: multiple products can share a category
    result = prd_info.merge(
        px_cat_g1v2,
        how="left",
        left_on="cat_key",
        right_on="id",
        validate="many_to_one",
    )

    # Select the fields required by the final product dimension.
    result = result[
        [
            "prd_id",
            "prd_key",
            "cat_key",
            "prd_nm",
            "prd_cost",
            "prd_line",
            "prd_start_dt",
            "prd_end_dt",
            "cat",
            "subcat",
            "maintenance",
        ]
    ]

    # Rename source fields to the final dimension naming conversion.
    result = result.rename(
        columns={
            "prd_id": "product_id",
            "prd_key": "product_code",
            "cat_key": "category_key",
            "prd_nm": "product_name",
            "prd_cost": "product_cost",
            "prd_line": "product_line",
            "prd_start_dt": "start_date",
            "prd_end_dt": "end_date",
            "cat": "category",
            "subcat": "subcategory",
        }
    )

    return result