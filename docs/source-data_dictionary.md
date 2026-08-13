# 📂Source data dictionary

## Overview
Before deciding how to transform and model the data, we need a clear picture of what the source data actually looks like.

### Remark
The data types are derived obtained using pandas library, so the format mayber different from what you know (e.g. int maybe int64...)

---

### **1. cust_info** 
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

### **2. prd_info** 
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

### **3. sales_details** 
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

### **4. CUST_AZ12** 
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

### **5. LOC_A101** 
- **Purpose:** Stores customers geographic details.
- **Rows:** ~18484
- **Header:** Yes
- **Duplicates:** 0

| Column Name   | Data Type     | Column Type   | Nulls     | Unique        | Example             |
|---------------|---------------|---------------|-----------|---------------|---------------------|
| CID*          | str           | text          | 0         | True          | 'AW-00019294'       |
| CNTRY         | str           | text          | 332       | False         | 'Germany'           |

---

### **6. PX_CAT_G1V2** 
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
