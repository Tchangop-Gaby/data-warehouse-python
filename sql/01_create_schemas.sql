/*
============================================================================
Database Schemas
============================================================================

Description:
    Creates the schemas required by the data warehouse pipeline.

Schemas:
    staging     - Stores raw or temporarily extracted source data.
    warehouse   = Stores transformed dimensional and fact data for analysis.
    quality     - Stores data quality checks and their results.

Behavior:
    Schemas are created only if they do not already exist.
*/

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS quality;