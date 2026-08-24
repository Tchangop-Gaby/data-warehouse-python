/*
============================================================================
Warehouse Schema DDL
============================================================================

Purpose:
    Define and initializes the dimensional and fact tables used by
    the data warehouse, including their constraints and performance
    indexes

Description:
    This file contains the Data Definition Language (DDL) statements
    required to create and initialize the warehouse schema.

    It include:
        - Dimension tables used to store descriptive business
            information.
        - Fact Tables used to store measurable business events.
        - Primary and foreign key constraints
        - Default/unknown records used when source data is missing
            or cannot ne matched to a dimension.
        - Indexes on frequently queried fact table columns to imporve
            query performance

Schema: 
    warehouse

Main Components:

    Dimensions:
        - dim_customer: Stores Customers information used for
            customers/business analysis
        - dim_product: Stores Product information used for
            product analysis
        - dim_date: Stores calendar information used for 
            date-based analysis.

    Facts:
        - fact_sales: Stores sales transactions and links
            each transaction to the relevant customer, product,
            and date dimensions.

    Behavior:
        - Tables are created only if thez do not already exist.
        - Dimension tables store descriptive attributes used 
            for analysis.
        - Fact tables store transactional and measurable 
            `business data.
        - Foreign keys maintain referential integrity between
            fact and dimension tables.
        - Default "Unknown" records provide valid dimension keys
            when source data is missing or cannot be matched.
        - Indexes improve query performance when filtering or joining
            fact date using customer, product, or date key.
        - CREATE INDEX IF NOT EXISTS allows the script to be safely 
            re-executed without attempting to recreate existing indexes.
*/

CREATE TABLE IF NOT EXISTS warehouse.dim_customer (
    customer_key BIGSERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    customer_code VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    gender VARCHAR(20),
    marital_status VARCHAR(20),
    country VARCHAR(100),
    create_date DATE,
    dwh_load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_dim_customer_customer_id
        UNIQUE (customer_id)
);
INSERT INTO warehouse.dim_customer (
    customer_key,
    customer_id,
    customer_code,
    first_name,
    last_name,
    birth_date,
    gender,
    marital_status
)
VALUES (
    0,
    -1,
    'UNKNOWN',
    'Unknown',
    'Unknown',
    NULL,
    'Unknown',
    'Unknown',
    'Unknown'
)
ON CONFLICT (customer_key) DO NOTHING;

CREATE TABLE IF NOT EXISTS warehouse.dim_product (
    product_key BIGSERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_code VARCHAR(50),
    product_name VARCHAR(100),
    product_cost NUMERIC(18,2),
    product_line VARCHAR(50),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    maintenance VARCHAR(100),
    start_date DATE,
    end_date DATE,
    dwh_load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_dim_product_id 
        UNIQUE (product_id)
);
INSERT INTO warehouse.dim_product (
    product_key,
    product_id,
    product_code,
    product_name,
    product_cost,
    product_line,
    category,
    subcategory,
    maintenace
)
VALUES (
    0,
    -1,
    'UNKNOWN',
    'Unknown',
    0,
    'Unknown',
    'Unknown',
    'Unknwon',
    'Unknown'
)
ON CONFLICT (product_key) DO NOTHING;

CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_of_month INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20)NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    month_number INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INTEGER NOT NULL,
    year_number INTEGER NOT NULL,
    week_number INTEGER NOT NULL
);
INSERT INTO warehouse.dim_date (
    date_key,
    full_date,
    day_of_month,
    day_of_week,
    day_name,
    day_name,
    month_number,
    month_name,
    quarter_number,
    year_number,
    week_number
)
VALUES (
    0,
    DATE '1900-01-01',
    1,
    1,
    'Unknown',
    1,
    'Unknown',
    1,
    1900,
    1
)
ON CONFLICT (date_key) DO NOTHING;

CREATE TABLE IF NOT EXISTS warehouse.fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(50),
    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    order_date_key INTEGER NOT NULL,
    ship_date_key INTEGER NOT NULL,
    due_date_key INTEGER NOT NULL,
    quantity INTEGER,
    unit_price NUMERIC(18.2),
    sales_amount NUMERIC(18,2),
    dwh_load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

    CONSTRAINT fk_fact_customer
        FOREIGN KEY (customer_key) REFERENCES warehouse.dim_customer(customer_key),

    CONSTRAINT fk_fact_product
        FOREIGN KEY (product_key) REFERENCES warehouse.dim_product(product_key),

    CONSTRAINT fk_order_date
        FOREIGN KEY (order_date_key) REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_ship_date
        FOREIGN KEY (ship_daate_key) REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_due_date
        FOREIGN KEY (due_date_key) REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT uq_fact_sales_order_product
        UNIQUE (order_number, product_key)
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer
ON warehouse.fact_sales(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product 
ON warehouse.fact_sales(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_order_date
ON warehouse.fact_sales(order_date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_ship_date
ON warehouse.fact_sales(ship_date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_due_date
ON warehouse.fact_sales(due_date_key);
