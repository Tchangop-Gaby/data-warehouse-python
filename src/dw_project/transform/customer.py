"""
Customer Data Transformation
============================

Purpose:
    Clean, standardize, reconcile, and combine 
    customer-related datasets into a single 
    customer dimension dataset.

Description:
    This module transforms customer data from the 
    cust_info, CUST_AZ12, and LOC_A101 source datasets.
    It standardizes columns and values, validates 
    business keys, reconciles customer identifiers, 
    normalizes demographic and geographic values, and 
    merges the datasets into the final customer structure.

Components:
    reconcile_keys(): 
        customer identifiers across source datasets
    normalize_gender():
        Standardizes gender values.
    normalize_marital_status():
        Standardizes marital status values.
    normalize_country():
        Standardizes country values.
    transform_customer():
        Executes the complete customer transformation.

Dependencies:
    common:
        Provides shared validation, column standardization,
        date conversion, and data cleansing utilities.
"""
import pandas as pd

from .common import (
    validate_unique_key,
    standardize_columns,
    convert_dates,
    standardize_data,
)

def reconcile_keys(
        cust_az12: pd.DataFrame,
        loc_a101: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Standardize customer identifiers used by auxiliary datasets.

    Args:
        cust_az12: Customer demographic DataFrame.
        loc_a101: Customer location DataFrame.
    
    Returns:
        Tuples containing the normalized CUST_AZ12 and LOC_A101 
        DataFrames.
    """
    cust_az12 = cust_az12.copy()
    loc_a101 = loc_a101.copy()

    cust_az12["cid"] = cust_az12["cid"].fillna("").astype(str).str.strip().str.upper()
    loc_a101["cid"] = loc_a101["cid"].fillna("").astype(str).str.strip().str.upper()

    # Remove the NAS prefix used in location identifiers.
    cust_az12.loc[
        cust_az12["cid"].str.startswith("NAS", na=False),
        "cid",
    ] = (
            cust_az12.loc[
            cust_az12["cid"].str.startswith("NAS", na=False),
            "cid",
            ].str.replace("NAS", "", regex=False).str.strip()
        )

    # Remove separators so auxiliary keys match the customer key format.
    loc_a101["cid"] = loc_a101["cid"].str.replace("-","", regex=False)

    return cust_az12, loc_a101

def normalize_gender(values: pd.Series) -> pd.Series:
    """
    Normalize gender values to a consistent representation.

    Args:
        values: Series containing raw gender values.

    Returns:
        Series containing stadardized gender values or "Unknown".
    """
    values = values.fillna("").astype(str).str.strip().str.upper()

    return values.map({
        "M": "Male",
        "MALE": "Male",
        "F": "Female",
        "FEMALE": "Female",
    }).fillna("Unknown")

def normalize_marital_status(values: pd.Series) -> pd.Series:
    """
    Normalize marital status values to a consistent representation.

    Args:
        values: Series containing raw marital status values.

    Returns:
        Series containing stadardized marital status values or "Unknown".
    """
    values = values.fillna("").astype(str).str.strip().str.upper()

    return values.map({
        "S": "Single",
        "M": "Married",
    }).fillna("Unknown")

def normalize_country(values: pd.Series) -> pd.Series:
    """
    Normalize country codes and names to standardized country names.

    Args:
        values: Series containing raw country values.

    Returns:
        Series containing stadardized country names or "Unknown".
    """
    values = values.fillna("").astype(str).str.strip().str.upper()

    return values.map({
        "DE": "Germany",
        "GERMANY": "Germany",
        "US": "United States",
        "USA": "United States",
        "AUSTRALIA": "Australia",
        "CANADA": "Canada",
        "FRANCE": "France",
        "UNITED KINGDOM": "United Kingdom",
    }).fillna("Unknown")

def transform_customer(
        cust_info: pd.DataFrame,
        cust_az12: pd.DataFrame,
        loc_a101: pd.DataFrame,
) -> pd.DataFrame:
    """
    Transform and combine customer source datasets.

    The transformation standardizes the input schemas, 
    validates business keys, reconciles identifiers, 
    normalizes customer attributes, merges demographic 
    and location data, and produces the final customer 
    dataset

    Args:
        cust_info: Primary customer information DataFrame.
        cust_az12: Customer demographc DataFrame.
        loc_a101: Customer location DataFrame.

    Returns:
        DataFrame containing the transformed customer dimension data.

    Raises:
        ValueError: If any source contains duplicate values for its
        expected unique business key.
    """

    # Standardize source column names before applying transformations
    cust_info = standardize_columns(cust_info).copy()
    cust_az12 = standardize_columns(cust_az12).copy()
    loc_a101 = standardize_columns(loc_a101).copy()

    # Remove non-identified customer values.
    cust_info = cust_info.dropna(subset=["cst_key"])
    cust_az12 = cust_az12.dropna(subset=["cid"])
    loc_a101 = loc_a101.dropna(subset=["cid"])

    # Remove duplicated customer values
    cust_info = cust_info.drop_duplicates(subset=["cst_key"], keep="first")
    cust_az12 = cust_az12.drop_duplicates(subset=["cid"], keep="first")
    loc_a101 = loc_a101.drop_duplicates(subset=["cid"], keep="first")

    # Validate source business keys before perofrming the joins.
    cust_az12, loc_a101 = reconcile_keys(
        cust_az12,
        loc_a101,
    )
    
    validate_unique_key(
        cust_info,
        "cst_key",
        "cust_info",
    )

    validate_unique_key(
        cust_az12,
        "cid",
        "CUST_AZ12",
    )

    validate_unique_key(
        loc_a101,
        "cid",
        "LOC_A101"
    )

    # Convert data fields to a consistent datetime representation.
    cust_info["cst_create_date"] = convert_dates(cust_info["cst_create_date"])
    cust_az12["bdate"] = convert_dates(cust_az12["bdate"])

    # Normalize customer demographic attributes.
    cust_info["cst_gndr"] = normalize_gender(cust_info["cst_gndr"])
    cust_az12["gen"] = normalize_gender(cust_az12["gen"])
    cust_info["cst_marital_status"] =  normalize_marital_status(cust_info["cst_marital_status"])

    # Normalize location attributes
    loc_a101["cntry"] = normalize_country(loc_a101["cntry"])

    # Clean customer names before combining the datasets.
    cust_info["cst_firstname"] = standardize_data(cust_info["cst_firstname"])
    cust_info["cst_lastname"] = standardize_data(cust_info["cst_lastname"])

    # Add demographic information to the primary customer dataset.
    result = cust_info.merge(
        cust_az12,
        how="left",
        left_on="cst_key",
        right_on="cid",
        validate="one_to_one",
    )

    # Add location information using the reconciled customer key.
    result = result.merge(
        loc_a101,
        how="left",
        left_on="cst_key",
        right_on="cid",
        validate="one_to_one",
    )

    # Select and order the fields required by the customer dimension.
    result = result[
        [
            "cst_id",
            "cst_key",
            "cst_firstname",
            "cst_lastname",
            "cst_marital_status",
            "cst_gndr",
            "cst_create_date",
            "bdate",
            "gen",
            "cntry",
        ]
    ]

    # Rename source-specific fields to the final dimension naming convention.
    result = result.rename(
        columns={
            "cst_id": "customer_id",
            "cst_key": "customer_key",
            "cst_firstname": "first_name",
            "cst_lastname": "last_name",
            "cst_marital_status": "marital_status",
            "cst_gndr": "gender",
            "cst_create_date": "create_date",
            "bdate": "birth_date",
            "gen": "aux_gender",
            "cntry": "country",
        }
    )

    return result