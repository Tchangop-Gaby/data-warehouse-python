# 🚀 Data Warehouse Engineering Project

## 📃 Overview

This project impleents an end-to-end data warehouse pipeline that extracts data from six local CSV files, loads the data into PostgreSQL staging tables, transforms and validates the data using Python and Pandas, builds a dimensional warehouse model, and expose business-oriented analytical models through a dedicated analitycs schema.

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Pytest
- SQL

## 📈 Business Problem
The source data is distributed in CRM and ERP szstems across multiple CSV files representing customers, customer demographics, locations, products, products category, and sales transaction. The objective is to integrate these heterogeneous sources into a centralized relational data warehouse that supports consistent reporting and analytical queries.

Read more: [Business Requirement](docs/business/business_requirements.md)

```
Problem:
- Multiple CSV files.
- Different structures
- Different naming conventions.
- Data-quality issues
- Difficult direct analysis.

Solution (DData Warehouse):
Integrated, Validated, Consistent, and Analytics-ready data.
```

## 📘 Source Data

| File | Purpose |
|---|---|
| cust_info | Customer master data |
| prd_info | Product master data |
| sales_details | Sales transactions |
| CUST_AZ12 | Customer demographic data |
| LOC_A101 | Customer location |
| PX_CAT_G1V2 | Product categorization |

![Data Integration](docs/Source/Data%20Integration.png)

Read more: [Source Data Documentation](docs/Source/source-data%20documentation.md)

## Data Architecture
![Data Architecture](docs/Data%20Architecture.png)

## Warehouse Schema
![Star Schema](docs/data-model/Star%20Schema.png)

## 📃 Dimensional Tables

| Table | Source |
|---|---|
| dim_customer | cust_info, CUST_AZ12, LOC_A101 |
| dim_product | prd_info, PX_CAT_G1V2 |
| dim_date | sales_details(order, ship, and due) |

## ⚙ Transforamtion/Data Quality Rules

See:
[Transformation and Mapping](docs/transformation/transformation%20and%20mapping%20.md),
[Quality-Check Rules](docs/transformation/Quality-check%20rules%20.md)

## 📊 Analytics Layer

The analytics schema provides business-oriented views over  the dimensional warehouse. Rather than exposing the underlying warehouse model directly to customers, the analytics layer provides simplified datasets containing commonly used KPIs and aggregations.
```
analytics.sales_daily
analytics.sales_monthly
analytics.rpdocut_performance
analytics.customer_perofrmance
analytics.category_performance
analytics.sales_by_country
```

## 🏗 Project Structure

```
data-warehouse-python
│
├── data/                   # Source CRM and ERP CSV files
├── docs/                   # Documents describing the project
├── logs/                   # Pipeline execution logs
├── sql/                    # Database DDL and analytical SQL
├── src/                    # Python application
├── tests/                  # Automated tests
├── .env.example            # Placeholders for Database credentials            
├── main.py                 # Main pipeline execution file
├── pyproject.toml          # Project settings         
├── README.md               # Project Documentation
├── requirements.txt        # Required Project Packages
```

## 🛠 How to Run
1. `git clone <repository>`
2. `cd data_warehouse_python`
3. Create environment: `python -m venv .venv`
4. Activate it: `.venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Configure a Postgres Server, and create a database.
6. Configure .env.example
7. Run the sql scripts in PostgreSQL.
8. Run: `pip install -e .`
9. Run: `python -m main.py`
10. Run: `python -m pytest`


## 📑 Design Decision

### Whx Pandas?
Small, static CSV dataset and single-machine processing.

### Whz PostgreSQL?
Open-source relational database with strong SQL and dimensional-modeling support.

### Why staging?
Seperates ingestion from transformation and warehouse modeling.

### Why star schema?
Provides a simple analytical structure around measurable sales events.

### Why surrogate keys?
Decouples warehouse dimensions from source-system identifiers.

### Why no incremental loading?
Source files are static and processed once.

### Why analytics views?
Avoid unnecessary data duplicationg while providing business-friendly models.

### Why pytest?
Provides automated validation of transformation logic and pipeline behavior.

---

## 🌟 About Me

Hi there! I'm **Tchangop Pieumi Gaby Junior**. I'm an Aspiring Data Engineer building Data Projects to gain Hand-on skills to be able to excel in the exciting world of Data

Let's stay in touch! Feel free to connect with me on the following platform:
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gaby-tchangop?utm_source=share_via&utm_content=profile&utm_medium=member_android)

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and share this project with proper attribution.
