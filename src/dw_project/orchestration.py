import logging
from pathlib import Path
from sqlalchemy.engine import Engine

from .config import (
    SOURCE_FILES,
    EXPECTED_COLUMNS,
)

from .extract.csv_loader import (
    load_csv,
    validate_columns,
)

from .database import (
    create_db_engine
)

from .load.staging import (
    truncate_staging_table,
    load_dataframe_to_staging,
)

logger = logging.getLogger(__name__)

def run_pipeline():

    logger.info("Pipeline started")

    extraction_stage()

    # staging_stage()

    # transformation_stage()

    # dimension_stage()

    # fact_stage()

    # validation_stage()

    logger.info("Pipeline completed")


def extraction_stage() -> dict:

    logger.info("Staging extraction stage")

    results = {}

    for source_file in SOURCE_FILES:

        file_path = Path("data\\raw", source_file.source_system, source_file.filename)

        logger.info(f"Extracting data from {file_path}")

        result = load_csv(file_path)

        logger.info(f"Validating data...")

        validate_columns(result.dataframe, EXPECTED_COLUMNS[source_file.filename])

        logger.info(f"   Columns: {result.column_count}")
        logger.info(f"   Rows: {result.row_count}")

        results[source_file.staging_table] = result

    logger.info("Extraction stage completed")

    return results

def transformation_stage():
    ...

def dimension_stage():
    ...

def fact_stage():
    ...

def validation_stage():
    ...