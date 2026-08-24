/*
============================================================================
Data Quality Results
============================================================================

Description:
    Stores the results of data quality checks performed by the pipeline.

Purpose:
    Provides an audit trails of quality checks, including their status,
    severity, number of rows checked/failed, and any associated errors.

Key Fields:
    run_id          - Identifies the pieline execution
    check_id        - Unique identifier of the quality check.
    check_name      - Name/description of the quality check.
    table_name      - Table on which the check was performed.
    severity        - Check severity INFO, WARNING, or ERROR.
    status          - Result of the check: PASS or FAIL.
    rows_checked    - Number of rows evaluated.
    rows_failed     - Number of rows that failed the check.
    error_message   - Details of the failure, if applicable.
    checked_at      - Timestamp when the check was performed.
*/

CREATE TABLE IF NOT EXISTS quality.data_quality_results (
    quality_result_id BIGSERIAL PRIMARY KEY,
    run_id VARCHAR(100) NOT NULL,
    check_id VARCHAR(100) NOT NULL,
    check_name VARCHAR(200) NOT NULL,
    table_name VARCHAR(100),
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20),
    rows_checked BIGINT,
    rows_failed BIGINT,
    error_message TEXT,
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_quality_severity
        CHECK (severity IN ('INFO', 'WARNING', 'ERROR'))

    CONSTRAINT chk_quality_status
        CHECK (status IN ('PASS', 'FAIL'))
);