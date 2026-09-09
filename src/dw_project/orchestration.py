import logging

logger = logging.getLogger(__name__)

def run_pipeline():

    logger.info("Pipeline started")

    extraction_stage()

    staging_stage()

    transformation_stage()

    dimension_stage()

    fact_stage()

    validation_stage()

    logger.info("Pipeline completed")


def extraction_stage():
    ...

def staging_stage():
    ...

def transformation_stage():
    ...

def dimension_stage():
    ...

def fact_stage():
    ...

def validation_stage():
    ...