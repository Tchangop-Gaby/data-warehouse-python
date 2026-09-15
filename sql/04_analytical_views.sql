/*
 Analytics Views
 ===============
 
 Purpose:
 Provide reusable analytical views for reporting
 and business analysis
 
 Description:
 Creates aggregated views over the warehouse fact 
 and dimension tables to support sales, product,
 category, customer, demographic, and geographic 
 analysis at different levels of detail.
 */
CREATE VIEW analytics.sales_summary AS
SELECT COUNT(DISTINCT order_number) AS total_orders,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales,
    AVG(sales_amount) AS average_order_line_value,
    AVG(unit_price) AS average_unit_price
FROM warehouse.fact_sales;
CREATE VIEW analytics.sales_daily AS
SELECT d.full_date,
    d.year_number,
    d.month_number,
    d.month_name,
    COUNT(DISTINCT f.order_number) AS total_orders,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_sales,
    (
        SUM(sales_amount) / NULLIF(COUNT(DISTINCT order_number), 0)
    ) AS average_order_value
FROM warehouse.fact_sales f
    JOIN warehouse.dim_date d ON f.order_date_key = d.date_key
GROUP BY d.full_date,
    d.year_number,
    d.month_number,
    d.month_name;
CREATE VIEW analytics.sales_monthly AS
SELECT d.year_number,
    d.month_number,
    d.month_name,
    COUNT(DISTINCT f.order_number) AS total_orders,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_sales,
    (
        SUM(sales_amount) / NULLIF(COUNT(DISTINCT order_number), 0)
    ) AS average_order_value
FROM warehouse.fact_sales f
    JOIN warehouse.dim_date d ON f.order_date_key = d.date_key
GROUP BY d.year_number,
    d.month_number,
    d.month_name;
CREATE VIEW analytics.product_performance AS
SELECT p.product_key,
    p.product_code,
    p.product_name,
    p.category,
    p.subcategory,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.sales_amount) AS total_sales,
    COUNT(DISTINCT f.order_number) AS total_orders,
    AVG(f.unit_price) AS average_selling_price
FROM warehouse.fact_sales f
    JOIN warehouse.dim_product p ON f.product_key = p.product_key
GROUP BY p.product_key,
    p.product_code,
    p.product_name,
    p.category,
    p.subcategory;
CREATE VIEW analytics.category_performance AS
SELECT p.category,
    p.subcategory,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.sales_amount) AS total_sales,
    COUNT(DISTINCT f.order_number) AS total_orders,
    AVG(f.unit_price) AS average_selling_price
FROM warehouse.fact_sales f
    JOIN warehouse.dim_product p ON f.product_key = p.product_key
GROUP BY p.category,
    p.subcategory;
CREATE VIEW analytics.customer_performance AS
SELECT c.customer_key,
    c.customer_code,
    c.first_name,
    c.last_name,
    c.gender,
    c.marital_status,
    c.country,
    COUNT(DISTINCT f.order_number) AS total_orders,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_sales,
    (
        SUM(f.sales_amount) / NULLIF(COUNT(DISTINCT f.order_number), 0)
    ) AS average_order_value
FROM warehouse.fact_sales f
    JOIN warehouse.dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_key,
    c.customer_code,
    c.first_name,
    c.last_name,
    c.gender,
    c.marital_status,
    c.country;
CREATE VIEW analytics.sales_by_country AS
SELECT c.country,
    COUNT(DISTINCT c.customer_key) AS total_customers,
    COUNT(DISTINCT f.order_number) AS total_orders,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_sales
FROM warehouse.fact_sales f
    JOIN warehouse.dim_customer c ON f.customer_key = c.customer_key
GROUP BY country;
CREATE VIEW analytics.sales_by_gender AS
SELECT c.gender,
    COUNT(DISTINCT c.customer_key) AS customers,
    COUNT(DISTINCT f.order_number) AS orders,
    SUM(f.sales_amount) AS sales
FROM warehouse.fact_sales f
    JOIN warehouse.dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.gender;