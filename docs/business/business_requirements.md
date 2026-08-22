# 📃 Business Requirements Document

## **Business Scenario**
> The company wants a centralized data warehouse for analyzing sales perdformance, customers, products, and product categories over time.

---

## **Table of Content**
1. [Analytical Users](#analytical-users)
    - [Sales management](#sales-management)
    - [Product management](#product-management)
    - [Customer and business analysis](#customer-and-business-analysis)
2. [Business questions](#business-questions)
    - [Sales performance](#sales-performance)
    - [Product performance](#product-performance)
    - [Customers performance](#customers-performance)
3. [KPIs and metrics](#kpis-and-metrics)
4. [Analytical Dimensions](#analytical-dimensions)
5. [Scope](#scope)

## **Analytical Users**

### Sales management
- How much are we selling?
- How are sales changing over time?
- Which products perform best?
- Which customers generate the most revenue?

### Product management
- Which products sell the most?
- Which product categories perform best?
- Which subcategories generate the most revenue?
- How do product costs compare with sellin prices?

### Customer and business analysis
- What are our highest-value customers?
- How much does each customer purchase?
- Where are our customers located?
- How do demographics relate to sales?

---

## **Business questions**

Not all the 15 following questiions will be implemented.

### Sales performance
1. What is the total sales revenue?
2. How many orders were placed?
3. How many products were sold?
4. What is the average order value?
5. How does revenue change over time?
6. How long does it take to ship an order?

### Product performance
7. Which products generate the most rev enue?
8. Which products have the highest sales volume?
9. Which product categories generate the most revenue?
10. Which subcategories perform best?

### Customers performance
11. Which customers generate the most revenue?
12. How many orders does each customer place?
13. What is the average revenue per countries?
14. How does revenue vary by customer country?
15. How does the customer gender or age relate to sales?

---

## **KPIs and metrics**

| KPI / Metric          | Definition                                |
|-----------------------|-------------------------------------------|
| Total revenue           | Sum of sales amount                       |
| Total Orders          | Number of distinct orders                   |
| Units Sold            | Sum of qunatities                         |
| Average Order Value   | Revenue / orders |
| Customer Sales        | Total sales attributed to a customer      |
| Product Sales         | Total sales attributed to a product       |

---

## **Analytical Dimensions**

| Dimension | Table |
|---|---|
| dim_customer | cust_info, CUST_AZ12, LOC_A101 |
| dim_product | prd_info, PX_CAT_G1V2 |
| dim_date | sales_details(sls_order_dt, sls_ship_dt, sls_due_dt) |

## **Scope**

### In scope
- Six local CSV files
- Batch extraction
- Pandas
- PostgreSQL
- Staging layer
- Transformation layer
- Data-quality checks
- Dimensional warehouse
- Analytics layer
- Logging
- Error handling
- Unit testing
- Data reconcialiation
- Documentaion

### Out of scope
- Incremental loading
- CDC
- Real-time streaming
- Kafka
- Spark/dbt
- Cloud infrastructure
- Distributed processing
- CXomplex orchestration