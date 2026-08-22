# 📂Source data dictionary

Before deciding how to transform and model the data, we need a clear picture of what the source data actually looks like.

## **Table of Contents**
1. [Remark](#remark)
2. [Inventory](#inventory)
3. [Data Quality Baseline](#data-quality-baseline)
    - [cust_info](#cust_info)
    - [prd_info](#prd_info)
    - [sales_details](#sales_details)
    - [CUST_AZ12](#cust_az12)
    - [LOC_A101](#loc_a101)
    - [PX_CAT_G1V2](#px_cat_g1v2)


## **Remark**
The data types are derived obtained using pandas library, so the format mayber different from what you know (e.g. int maybe int64...)

---

## **Inventory**
| File      | Business meaning | Grain | Rows | Columns | Candidate PKs | Candidate FKs |
|---|---|---|---|---|---|---|
| cust_info | Customers Information | One row per customer | 18495 | 7 | cst_id | cst_key |
| prd_info | Products Information | One row per product | 398 | 7 | prd_id | prd_key |
| sales_details | Orders Details | One row per order-product line | 60398 | 9 | sls_ord_num | sls_prd_key, sls_cust_id | 
| CUST_AZ12 | Customers Biographic Information | One row per customer | 18484 | 3 | CID | None | 
| LOC_A101 | Customers Geographic Information | One row per customer | 18484 | 2 | CID | None |
| PX_CAT_G1V2 | Product Category Information | One row per product/category | 37 | 4 | ID | None |

## **Data Quality Baseline**

### **cust_info** 
- **Purpose:** Stores some customers details (demography and geographic information in CUST_AZ12 and LOC_A101)'
- **Rows:** ~18495
- **Header:** Yes
- **Duplicates:** 9

| Column Name           | Data Type     | Column Type   | Nulls    | Unique    | Exaample       |
|-----------------------|---------------|---------------|----------|-----------|----------------|
| cst_id*               | float64       | numeric       | 4        | False     | 11057          |
| cst_key*              | str           | text          | 0        | False     | 'AW00011057'   |
| cst_firstname         | str           | text          | 8        | False     | 'Carl'         |
| cst_lastname          | str           | text          | 7        | False     | 'Andersen'     |
| cst_marital_status    | category      | text          | 7        | False     | 'M'            |
| cst_gndr              | category      | text          | 4578     | False     | 'M'            |
| cst_create_date       | str           | date          | 4        | False     | '2025-10-07'   |

---

### **prd_info** 
- **Purpose:** Store products details (category information in PX_CAT_G1V2).
- **Rows:** ~398
- **Header:** Yes
- **Duplicates:** 0

| Column Name   | Data Type     | Column Type   | Nulls     | Unique        | Example             |   
|---------------|---------------|---------------|-----------|---------------|---------------------|
| prd_id*       | int64         | numeric       | 0         | True          | 370                 |
| prd_key*      | str           | text          | 0         | False         | 'BI-RB-BK-R89R-52'  |
| prd_nm        | str           | text          | 0         | False         | 'Road-250 Red- 52'  |
| prd_cost      | float64       | numeric       | 2         | False         | 1519                |
| prd_line      | str           | category      | 17        | False         | 'R'                 |
| prd_start_dt  | str           | date          | 0         | False         | '2012-07-01'        |
| prd_end_dt    | str           | date          | 197       | False         | '2008-12-27'        |

---

### **sales_details** 
- **Purpose:** Stores the information on orders.
- **Rows:** ~60398
- **Header:** Yes
- **Duplicates:** 0

| Column Name   | Data Type     | Column Type   | Nulls     | Unique        | Example       |
|---------------|---------------|---------------|-----------|---------------|---------------|
| sls_ord_num*  | str           | text          | 0         | True          | 'SO43697'     |
| sls_prd_key   | str           | text          | 0         | False         | 'BK-R93R-62'  |
| sls_cust_id   | int64         | numeric       | 0         | False         | 21768         |
| sls_order_dt  | int64         | date          | 0         | False         | 20101229      |
| sls_ship_dt   | int64         | date          | 0         | False         | 20110105      |
| sls_due_dt    | int64         | date          | 0         | False         | 20110110      |
| sls_sales     | float64       | numeric       | 8         | False         | 3578          |
| sls_quantity  | int64         | numeric       | 0         | False         | 1             |
| sls_price     | float64       | numeric       | 7         | False         | 3578          |

---

### **CUST_AZ12** 
- **Purpose:** Stores customers demographic details.
- **Rows:** ~18484
- **Header:** Yes
- **Duplicates:** 0

| Column Name   | Data Type     | Column Type   | Nulls     | Unique        | Example             |
|---------------|---------------|---------------|-----------|---------------|---------------------|
| CID*          | str           | text          | 0         | True          | 'NASAW00011330'     |
| BDATE         | str           | date          | 0         | False         | '1945-11-10'        |
| GEN           | str           | category      | 1472      | False         | 'Male'              |

---

### **LOC_A101** 
- **Purpose:** Stores customers geographic details.
- **Rows:** ~18484
- **Header:** Yes
- **Duplicates:** 0

| Column Name   | Data Type     | Column Type   | Nulls     | Unique        | Example             |
|---------------|---------------|---------------|-----------|---------------|---------------------|
| CID*          | str           | text          | 0         | True          | 'AW-00019294'       |
| CNTRY         | str           | text          | 332       | False         | 'Germany'           |

---

### **PX_CAT_G1V2** 
- **Purpose:** Stores products categories and maintenance details.
- **Rows:** ~37
- **Header:** Yes
- **Duplicates:** 0

| Column Name   | Data Type     | Column Type   | Nulls     | Unique        | Example       |
|---------------|---------------|---------------|-----------|---------------|---------------|
| ID*           | str           | text          | 0         | True          | 'CL_SO'       |
| CAT           | str           | category      | 0         | False         | 'Clothing'    |
| SUBCAT        | str           | category      | 0         | False         | 'Socks'       |
| MAINTENANCE   | str           | category      | 0         | False         | 'No'          |
