import os 
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str

def get_database_config() -> DatabaseConfig:
    return DatabaseConfig(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=int(os.getenv("DATABASE_PORT", "5432")),
        database=os.getenv("DATABASE_NAME", ""),
        user=os.getenv("DATABASE_USER", ""),
        password=os.getenv("DATABASE_PASSWORD", ""),
    ) 

@dataclass(frozen=True)
class SourceFileConfig:
    source_system: str
    filename: str
    staging_table: str

SOURCE_FILES = (
    SourceFileConfig(
        source_system="crm/",
        filename="cust_info.csv",
        staging_table="crm_cust_info",
    ),
    SourceFileConfig(
        source_system="crm/",
        filename="prd_info.csv",
        staging_table="crm_prd_info",
    ),
    SourceFileConfig(
        source_system="crm/",
        filename="sales_details.csv",
        staging_table="crm_sales_details",
    ),
    SourceFileConfig(
        source_system="erp/",
        filename="CUST_AZ12.csv",
        staging_table="erp_cust_az12",
    ),
    SourceFileConfig(
        source_system="erp/",
        filename="LOC_A101.csv",
        staging_table="erp_loc_a101",
    ),
    SourceFileConfig(
        source_system="erp/",
        filename="PX_CAT_G1V2.csv",
        staging_table="erp_px_cat_g1v2"
    ),
)

EXPECTED_COLUMNS = {
    "cust_info.csv": [
        "cst_id",
        "cst_key",
        "cst_firstname",
        "cst_lastname",
        "cst_marital_status",
        "cst_gndr",
        "cst_create_date",
    ],
    "prd_info.csv": [
        "prd_id",
        "prd_key",
        "prd_nm",
        "prd_cost",
        "prd_line",
        "prd_start_dt",
        "prd_end_dt",
    ],
    "sales_details.csv": [
        "sls_ord_num",
        "sls_prd_key",
        "sls_cust_id",
        "sls_order_dt",
        "sls_ship_dt",
        "sls_due_dt",
        "sls_sales",
        "sls_quantity",
        "sls_price",
    ],
    "CUST_AZ12.csv": [
        "CID",
        "BDATE",
        "GEN",
    ],
    "LOC_A101.csv": [
        "CID",
        "CNTRY",
    ],
    "PX_CAT_G1V2.csv": [
        "ID",
        "CAT",
        "SUBCAT",
        "MAINTENANCE",
    ],
}