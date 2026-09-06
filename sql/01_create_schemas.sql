/*
============================================================================
Database Schemas
============================================================================

Description:
    Creates the schemas required by the data warehouse pipeline.

Schemas:
    staging     - Stores raw or temporarily extracted source data.
    warehouse   - Stores transformed dimensional and fact data for analysis.
    analytics   - Stores the analytical views. 

Behavior:
    Schemas are created only if they do not already exist.
*/

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS analytics;