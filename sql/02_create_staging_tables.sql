/*
===========================================================================
DDL: Staging Tables
===========================================================================

Purpose:
    Define all staging tables used by the data warehouse pipeline.

Schema: 
    staging

Description:
    This file contains the Data Definition Language (DDL) statemensts
    required to create the staging tables.

Behavior:
    - Creates tables only if they do not already exists.
    - Stores raw/extracted data before transformation.
    - Can be safely executed multiple times.

Tables:
    1. staging.erp_cust_info: Customers information
    2. staging.erp_prd_info: Products information
    3. staging.crm_sales_details: Orders information
    4. staging.erp_cust_az12: Customers demographic information
    5. staging.erp_loc_a101: Customers geographic information
    6. staging.erp_px_cat_g1v2: Products categories information
*/

CREATE TABLE IF NOT EXISTS staging.crm_cust_info (
    cst_id INTEGER,
    cst_key VARCHAR(50),
    cst_firstname VARCHAR(100),erp_
    cst_lastname VARCHAR(100),
    cst_marital_status VARCHAR(20),
    cst_gndr VARCHAR(20),
    cst_create_date DATE
);

CREATE TABLE IF NOT EXISTS staging.crm_prd_info (
    prd_id INTEGER,
    prd_key VARCHAR(50),
    prd_nm VARCHAR(100),
    prd_cost NUMERIC(18,2),
    prd_line VARCHAR(50),
    prd_start_dt DATE,
    prd_end_dt DATE
);

CREATE TABLE IF NOT EXISTS staging.crm_sales_details (
    sls_ord_num VARCHAR(50),
    sls_prd_key VARCHAR(50),
    sls_cust_id INTEGER,
    sls_order_dt DATE,
    sls_ship_dt DATE,
    sls_due_dt DATE,
    sls_sales NUMERIC(18, 2),
    sls_quantity INTEGER,
    sls_price NUMERIC(18, 2)
);

CREATE TABLE IF NOT EXISTS staging.erp_cust_az12 (
    CID VARCHAR(50),
    BDATE DATE,
    GEN VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS staging.erp_loc_a101 (
    CID VARCHAR(50),
    CNTRY VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS staging.erp_px_cat_g1v2 (
    ID VARCHAR(50),
    CAT VARCHAR(100),
    SUBCAT VARCHAR(100),erp_
    MAINTENANCE VARCHAR(20)
);