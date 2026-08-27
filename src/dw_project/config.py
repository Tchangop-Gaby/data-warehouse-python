"""
Application Configuration
=========================

Purpose:
    Define and load database and source-file
    configuration for the ETL pipeline.

Description:
    Loads database connection settings from environment
    variables and defines the source files, staging tables,
    and expected CSV schema used during data extraction
    and loading.

Components:
    DatabaseConfig:
        Stores database connection settings.
    get_database_config():
        Loads database settings from environment variables.
    validate_database_config():
        Validates required database settings.
    SourceFileConfig:
        Maps source files to staging tables.
    SOURCE_FILES:
        Define the source files used by the pipeline.
    EXPECTED_COLUMNS:
        Defines the expected schema for each source file.

Environmet Variables:
    DATABASE_HOST: Database server hostname, Defaults to localhost.
    DATABASE_PORT: Database server port. Defaults to 5432.
    DATABASE_NAME: Database name.
    DATABASE_USER: Database username.
    DATABASE_PASSWORD: Database password.
"""
import os 
from dataclasses import dataclass
from dotenv import load_dotenv

# Load database configuration from the .env file into the environment.
load_dotenv()

@dataclass(frozen=True)
class DatabaseConfig:
    """
    Stores database connection configuration.
    """
    host: str
    port: int
    database: str
    user: str
    password: str

def get_database_config() -> DatabaseConfig:
    """
    Load database configuration from environment variables.

    Returns:
        DatabaseConfig containing the database connection settings.
    """
    return DatabaseConfig(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=int(os.getenv("DATABASE_PORT", "5432")),
        database=os.getenv("DATABASE_NAME", ""),
        user=os.getenv("DATABASE_USER", ""),
        password=os.getenv("DATABASE_PASSWORD", ""),
    ) 

def validate_database_config(config: DatabaseConfig) -> None:
    """
    Validate that all required database settings are provided.

    Args:
        config: Database configuration to validate.
    
    Returns:
        ValueError: If one or more required settings are missing.
    """
    required_fields = {
        "DATABASE_HOST": config.host,
        "DATABASE_PORT": config.port,
        "DATABASE_NAME": config.database,
        "DATABASE_USER": config.user,
        "DATABASE_PASSWORD": config.password, 
    }

    missing_fileds = [
        name for name, value in required_fields.items()
        if value in ("", None)
    ]

    if missing_fileds:
        raise ValueError(f"Missing required database configuration: {','.join(missing_fileds)}")
    
@dataclass(frozen=True)
class SourceFileConfig:
    """
    Map a source file to its corresponding staging table.
    """
    source_system: str
    filename: str
    staging_table: str

# Source files and their corresponding staging tables.
SOURCE_FILES = (
    SourceFileConfig(
        source_system="source_crm",
        filename="cust_info.csv",
        staging_table="crm_cust_info",
    ),
    SourceFileConfig(
        source_system="source_crm",
        filename="prd_info.csv",
        staging_table="crm_prd_info",
    ),
    SourceFileConfig(
        source_system="source_crm",
        filename="sales_details.csv",
        staging_table="crm_sales_details",
    ),
    SourceFileConfig(
        source_system="source_erp",
        filename="CUST_AZ12.csv",
        staging_table="erp_cust_az12",
    ),
    SourceFileConfig(
        source_system="source_erp",
        filename="LOC_A101.csv",
        staging_table="erp_loc_a101",
    ),
    SourceFileConfig(
        source_system="source_erp",
        filename="PX_CAT_G1V2.csv",
        staging_table="erp_px_cat_g1v2"
    ),
)

# Expected column names for each source file.
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