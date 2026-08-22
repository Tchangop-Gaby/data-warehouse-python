# Transformation & Mapping 

Before writing Pandas transformation code, define exactly how every source columns becomes a warehouse column and what business rule is applied.

---

## **Customer Transformation**

| Source | Target | Transforamtion |
|---|---|---|
| cst_id | customer_number | Validate non-nulls and non-duplicates |
| cst_key | customer_id | Trim |
| cst_firstname | first_name | Trim |
| cst_lastname | last_name | Trim |
| cst_marital_status | marital_status |Standardize |
| cst_gndr | gender | Standardize |
| cst_create_date | create_date | Date conversion |
| CUST_AZ12.CID | **join key** | Normalize |
| CUST_AZ12.BDATE | birth_date | Date conversion |
| CUST_AZ12.GEN | gender | Standardize/resolve |
| LOC_A101 | **join key** | Normalize |
| LOC_A101.CNTRY | country | Standardize |

## **Product Transformation**

| Sourrce | Target | Transformation |
|---|---|---|
| prd_id | product_id | Validate non-nulls and non-duplicates |
| prd_key | product_code | Trim + split |
| cat_id | category_code | Derive from prd_key |
| prd_nm | product_name | Trim |
| prd_cost | product_cost | Numeric conversion, validate >= 0 |
| prd_line | product_line | Standardize |
| prd_start_date | start_date | Date conversion |
| prd_end_date | end_date | Data conversion |
| PX_CAT_G1V2.ID | **join key** | Normalize |
| PX_CAT_G1V2.CAT | category | Trim/standardize |
| PX_CAT_G1V2.SUBCAT | subcategory | Trim/standardize |
| PX_CAT_G1V2.MAINTENANCE | maintenance | Standardize |

## **Sales transformation**
 
| Source | Target | Transformation |
|---|---|---|
| sls_ord_num | order_number | Validate  |
| sls_prd_key | product_key | Lookup dimension |
| sls_cust_id | customer_key | Lookup dimension |
| sls_order_dt | order_date_key | Date lookup |
| sls_ship_dt | ship_date_key | Date lookup |
| sls_due_dt | due_date_key | Date lookup |
| sls_quantity | quantity | Numeric , validate >= 0 |
| sls_price | unit_price | Numeric validation, validate >= 0 |
| sls_sales | sales_amount | Numeric validation, validate >= 0 |