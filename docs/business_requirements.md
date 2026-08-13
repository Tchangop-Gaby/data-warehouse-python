# 📃 Business Requirements Document

## 1. Project Overview
This project aims to build a batch data warehouse from CRM and ERP CSV source files. The piepline will extract and transform the source data using Python/Pandas, load the data into PostgreSQL staging tables, transform it into a dimensional warehouse containing facts and dimensions, and provide analytics-ready datasets through an analytics schema.

> The purpose is to centralize the source data and provide a consitent structure for analyzing business performance, customers, products, and transactions.

---

## 2. Business objectives
Centralize data from the CRM and ERP source systems, enabling analysis of sales eprformance, customer behavior, and product performance.

---

## 3. Business questions
### Sales
- What is the total sales amount?
- What are the monthly and yearly sales?
- What is the average order value?

### Products
- Which products generate the most revenue?
- Which products sell the most units?
- Which categories perform best?

### Customers
- Which customers generate the most revenue?
- How many orders does each customer make?
- What is the average customer spend?

### Geography
- Which countries generate the most sales?
- How does sales performance vary by location?

---

## 4. KPIs and metrics

| KPI / Metric          | Definition                                |
|-----------------------|-------------------------------------------|
| Total Sales           | Sum of sales amount                       |
| Total Orders          | Number of unique orders                   |
| Units Sold            | Sum of qunatities                         |
| Average Order Value   | Total sales / number of orders            |
| Customer Sales        | Total sales attributed to a customer      |
| Product Sales         | Total sales attributed to a product       |

---

## 5. Scope
### In scope
- CRM and ERP files
- Batch extraction
- Data cleaning and transformation
- PostgreSQL staging
- Dimensional warehouse
- Fact tables
- Dimensional tables
- Analytics schema
- Data quality validation
- Logging
- Error handling
- Testing
- Documentation

### Out of scope
- Incremental loading
- Change Data Capture (CDC)
- Real-time/streaming data
- Cloud deployment
- Production orchestration
- Airflow
- Spark
- Real-time dashboards

---

## 6. Business rules

### Customer rules
- Each customer should havea unique customer identifier.
- No Acronyms for categorical data.
- No extra spaces on customers first- and lastnames

### Product rules
- Each product should havea unique product identifier.
- The category id must be extracted from the product key.
- Product prices must not be negative.
- No Acronyms for categorical data.
- The product start dates must be less than the end dates.

### Order rules
- Each order must be associated with a valid customer and product.
- the order, ship, and due dates must follow an ascending order (due date > ship date > order date.)

### Sales rules
- Neither quantity nor unit price must be negative.
- Sales amount is calculated using quantity and unit price.

---

## 7. Expected outputs

### Warehouse
- `warehouse.dim_customer`
- `warehouse.dim_product`
- `warehouse.fact_sales`

### Analytics
- `analytics.monthly_sales`
- `analytics.product_performance`
- `analytis.customer_sales`
- `analytics.sales_by_country`
