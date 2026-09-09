from dw_project.logger_config import configure_logging

configure_logging()

from dw_project.orchestration import run_pipeline()

run_pipeline()