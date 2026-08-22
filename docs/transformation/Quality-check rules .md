# Quality-Check Rules

## **Three severity levels**

### ERROR
The pipeline should stop or the affected load should be rejected.

- Required key is NULL
- Duplicate primary business key
- Invalid date causing a required
- Lookup to fail
- Major referential-integrity
- failure
- . . .

### WARNING
The pipeline can continue, but the issue must be reported.

- Mssing birth date
- Mssing country
- Unknown category
- Small number of unmatched products
- . . .

### INFO
Informational statistics

- 30000 rows processed
- 5000 customers 
- 200 products
- 0 duplicate customers
- . . .

## **Catalog**
| Rule ID | Dataset | Rule | Severity |
|---|---|---|---|
| CUST-001 | Customer | **customer_id** not null | ERROR |
| CUST-002 | Customer | **customer_id** unique | ERROR |
| CUST-003 | Customer | Valid gender | WARNING |
| CUST-004 | Customer | Valid birth date | WARNING |
| CUST-005 | Customer | Country not null | WARNING |
| PROD-001 | Product | **product_code** not null | ERROR |
| PROD-002 | Product | **product_code** unique | ERROR |
| PROD-003 | Product | **product_cost** >= 0 | WARNING |
| PROD-004 | Product | Valid date range | WARNING |
| SALE-001 | Sales | **order_number** not null | ERROR |
| SALE-002 | Sales | Valid quantity | ERROR |
| SALE-003 | Sales | Valid sales amount | ERROR |
| SALE-004 | Sales | Order date <= ship date | WARNING |
| SALE-005 | Sales | Sales = quantity * price | WARNING |
| SALE-006 | Sales | Customer lookup succeeds | ERROR |
| SALE-007 | Sales | Product lookup succeeds | ERROR |
| SALE-008 | Sales | Sales grains unique | ERROR |

## **Quality results**
Store the quality check  results in a table which is loaded in a seperate schema in the database.

```
dq_results

run_id
check_id
table_name
check_name
severity
status
rows_checked
rows_failed
failure_percentage
execution_timestamp
```