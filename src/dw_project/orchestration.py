"""
Data Warehouse Pipeline
=======================

Purpose:
    Orchestrate the end-to-end ETL pipeline from raw CSV 
    extraction through staging, transformation, quality 
    validations, and warehouse loading.

Description:
    Coordinates each pipeline stage, tracks execution metrics, 
    logs progress, and stops the pipeline when transformation 
    quality checks fail.

Components:
    PipelineStatus:
        Tracks pipeline execution and data quality metrics.
    run_pipeline():
        Executes the complete ETL workflow.
    extraction_stage():
        Loads and validates raw CSV files.
    staging_loading_stage():
        Loads extracted data into staging tables.
    staging_extraction_stage():
        Read data back from staging tables.
    transformation_stage():
        Transfors customer, product, and sales data.
    quality_stage():
        Runs transformation data quality checks.
    dimension_stage():
        Builds and loads warehouse dimensions.
    fact_stage():
        Builds and loads the sales fact table.
    pipeline_summary():
        Logs a summary of the pipeline execution.
    
Exceptions:
    DataQualityError:
        Raised when transformation quality checks fail.
"""

from time import perf_counter
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

from .config import (
    SOURCE_FILES,
    EXPECTED_COLUMNS,
)
from .database import create_db_engine
from .extract.csv_loader import (
    load_csv,
    validate_columns,
)
from .extract.postgres import read_staging_table
from .load.staging import (
    truncate_staging_table,
    load_dataframe_to_staging,
)
from .load.load_dimensions import (
    COLUMNS,
    load_dimension,
)
from .load.fact_sales import (
    load_fact_sales,
    FACT_COLUMNS,
)
from .logger_config import (
    pipeline_logger,
    summary_logger,
)
from .quality.checks import (
    validate_customers,
    validate_products,
    validate_sales,
)
from .quality.runner import (
    quality_gate_passed,
    print_quality_report,
    summary_quality,
)
from .transform.common import add_surrogate_key
from .transform.customer import transform_customer
from .transform.product import transform_product
from .transform.date import create_date_dimension
from .transform.sales import (
    transform_sales, 
    prepare_fact_sales,
)

# ===========================================================
# Pipeline Configuration
# ===========================================================
db_engine = create_db_engine()

# ===========================================================
# Pipeline State and Exceptions
# ===========================================================
@dataclass
class PipelineStatus:
    """
    Track pipeline execution, row counts, 
    and quality check results.
    """
    status: str = "STARTED"

    extracted_rows: int = 0
    staging_rows: int = 0
    customer_rows: int = 0
    product_rows: int = 0
    fact_rows: int = 0

    total_quality_checks: int = 0
    quality_checks_passed: int = 0
    quality_checks_failed: int = 0

    duration: int = 0

class DataQualityError(Exception):
    """
    Raised when data quality validation fails.
    """

# ===========================================================
# Pipeline Orchestration
# ===========================================================
def run_pipeline():
    """
    Execute the complete data warehouse 
    ETL pipeline.
    """
    start = perf_counter()
    pipeline_status = PipelineStatus()

    pipeline_logger.info("=" * 70)
    pipeline_logger.info("DATA WAREHOUSE PIPELINE STARTED")
    pipeline_logger.info("=" * 70)

    data = extraction_stage(pipeline_status)

    staging_loading_stage(data, db_engine, pipeline_status)

    raw = staging_extraction_stage(db_engine)

    transformed = transformation_stage(raw)

    quality_stage(transformed, pipeline_status)

    dimensions = dimension_stage(transformed, db_engine, pipeline_status)

    fact_stage(transformed["sales"], dimensions, db_engine, pipeline_status)

    pipeline_logger.info("=" * 70)
    pipeline_logger.info("DATA WAREHOUSE PIPELINE COMPLETED")
    pipeline_logger.info("=" * 70)

    elapsed = perf_counter() - start

    pipeline_status.status = "SUCCESS"
    pipeline_status.duration = elapsed

    pipeline_summary(pipeline_status)

# ===========================================================
# 1. Extraction
# ===========================================================
def extraction_stage(pipeline_status: PipelineStatus) -> dict:
    """
    Extract and validate all configured 
    source CSV files.
    """
    pipeline_logger.info("Staging extraction stage")

    results = {}

    for source_file in SOURCE_FILES:

        file_path = Path("data\\raw", source_file.source_system, source_file.filename)

        pipeline_logger.info(f"Extracting data from {file_path}")

        result = load_csv(file_path)

        pipeline_logger.info(f"Validating data...")

        validate_columns(result.dataframe, EXPECTED_COLUMNS[source_file.filename])

        pipeline_logger.info(f"   Columns: {result.column_count}")
        pipeline_logger.info(f"   Rows: {result.row_count}")

        results[source_file.staging_table] = result

        pipeline_status.extracted_rows += result.row_count

    pipeline_logger.info("Extraction stage completed")

    return results

# ===========================================================
# 2. Staging Load
# ===========================================================
def staging_loading_stage(dict_of_data: dict, engine: Engine, pipeline_status: PipelineStatus) -> None:
    """
    Truncate and load extracted datasets into
    staging tables.
    """
    pipeline_logger.info("Starting staging load")

    for table_name, data in dict_of_data.items():

        pipeline_logger.info(f"Truncating {table_name}...")

        truncate_staging_table(table_name, engine)

        pipeline_logger.info(f"Loading {table_name[4:]} into {table_name}...")

        load_dataframe_to_staging(data.dataframe, table_name, engine)

        pipeline_logger.info(f"   Columns: {data.column_count}")
        pipeline_logger.info(f"   Rows: {data.row_count}")

        pipeline_status.staging_rows += data.row_count

    pipeline_logger.info("Staging load completed")

# ===========================================================
# 3. Staging Extraction
# ===========================================================
def staging_extraction_stage(engine) -> dict:
    """
    Read all configured datasets from the 
    staging tables.
    """
    pipeline_logger.info("Reading data from staging tables")

    dict_of_data = {}

    for source_file in SOURCE_FILES:

        pipeline_logger.info(f"Reading data from {source_file.staging_table}")

        dict_of_data[source_file.staging_table] = read_staging_table(source_file.staging_table, engine)

    pipeline_logger.info("Reading completed")

    return dict_of_data

# ===========================================================
# 4. Transformation
# ===========================================================
def transformation_stage(data: dict) -> dict:
    """
    Tranform customer, product, and sales datasets
    """
    pipeline_logger.info("Starting transformation stage")

    pipeline_logger.info(f"Transforming customers data")
    customer_df = transform_customer(
        data["crm_cust_info"],
        data["erp_cust_az12"],
        data["erp_loc_a101"],
    )

    pipeline_logger.info(f"Transforming products data")
    product_df = transform_product(
        data["crm_prd_info"],
        data["erp_px_cat_g1v2"],
    )

    pipeline_logger.info(f"Transforming sales data")
    sales_df = transform_sales(
        data["crm_sales_details"],
    )

    pipeline_logger.info("Transformation stage completed")

    return {
        "customer": customer_df,
        "product": product_df,
        "sales": sales_df,
    }

# ===========================================================
# 5. Data Quality
# ===========================================================
def quality_stage(transformed, pipeline_status: PipelineStatus):
    """
    Run transformation quality checks and enforce 
    the quality gate.
    """
    pipeline_logger.info("Starting trasnformation quality checks")

    customer_results = validate_customers(transformed["customer"])

    product_results = validate_products(transformed["product"])

    sales_results = validate_sales(transformed["sales"])

    all_results = (customer_results + product_results + sales_results)

    print_quality_report(all_results)

    if not quality_gate_passed(all_results):

        pipeline_logger.error("Data quality checks failed")

        raise DataQualityError("Transformation quality checks failed")

    pipeline_status.total_quality_checks = summary_quality(all_results)["total_checks"]
    pipeline_status.quality_checks_passed = summary_quality(all_results)["passed"]
    pipeline_status.quality_checks_failed = summary_quality(all_results)["failed"]

    pipeline_logger.info("All transformation quality checks passed")

# =======================================
# 6. Dimension Loading
# =======================================
def dimension_stage(trasnformed: dict, engine: Engine, pipeline_status: PipelineStatus) -> dict:
    """
    Build and load the customer, product, and date dimensions.
    """
    pipeline_logger.info("Starting dimension loading")

    customer_df = add_surrogate_key(trasnformed["customer"], "customer_id", "customer_key")
    product_df = add_surrogate_key(trasnformed["product"], "product_id", "product_key")
    date_df = create_date_dimension(trasnformed["sales"])

    load_dimension(customer_df, "dim_customer", COLUMNS["dim_customer"], engine)
    load_dimension(product_df, "dim_product", COLUMNS["dim_product"], engine)
    load_dimension(date_df, "dim_date", COLUMNS["dim_date"], engine)

    pipeline_status.customer_rows = len(customer_df)
    pipeline_status.product_rows = len(product_df)

    pipeline_logger.info("Dimension loading completed")

    return {
        "customer": customer_df,
        "product": product_df,
        "date": date_df,
    }

# =======================================
# 7. Fact Loading
# =======================================
def fact_stage(
        sales_df: pd.DataFrame,
        dimensions: dict,
        engine: Engine,
        pipeline_status: PipelineStatus,
) -> pd.DataFrame:
    """
    Prepare and load the sales fact dataset.
    """
    pipeline_logger.info("Starting fact transformation")

    fact_df = prepare_fact_sales(
        sales_df,
        dimensions["customer"],
        dimensions["product"],
        dimensions["date"],
    )

    pipeline_logger.info("Fact transformation completed")

    load_fact_sales(fact_df, engine)

    pipeline_status.fact_rows = len(fact_df)

    pipeline_logger.info("Fact loading completed")

    return fact_df

# =======================================
# 8. Pipeline Summary
# =======================================
def pipeline_summary(pipeline_status: PipelineStatus):
    """
    Log a summary of pipeline status, row counts, 
    and execution time.
    """
    summary_logger.info("=" * 70)
    summary_logger.info("PIPELINE SUMMARY")
    summary_logger.info("=" * 70)

    summary_logger.info("")

    summary_logger.info(f"Status: {pipeline_status.status}")

    summary_logger.info("")

    summary_logger.info(f"Extraction rows:      {pipeline_status.extracted_rows}")
    summary_logger.info(f"Staging rows:         {pipeline_status.staging_rows}")
    summary_logger.info(f"Customer rows:        {pipeline_status.customer_rows}")
    summary_logger.info(f"Product rows:         {pipeline_status.product_rows}")
    summary_logger.info(f"Fact rows:            {pipeline_status.fact_rows}")

    summary_logger.info("")

    summary_logger.info("Quality checks:")
    summary_logger.info(f"  Checks:   {pipeline_status.total_quality_checks}")
    summary_logger.info(f"  Passed:   {pipeline_status.quality_checks_passed}")
    summary_logger.info(f"  Failed:   {pipeline_status.quality_checks_failed}")

    summary_logger.info("")

    summary_logger.info(f"Duration: {pipeline_status.duration} seconds")

    summary_logger.info("=" * 70)

# =======================================
# Script Entry Point
# =======================================
if __name__ == "__main__":

    try:

        run_pipeline()

    except DataQualityError as exc:
        
        pipeline_logger.error(f"Pipeline stopped because data quality checks failed: {exc}")

        raise
    except Exception:

        pipeline_logger.exception("Pipeline failed unexpectedly")

        raise

