"""
Database Connection Managemnet
==============================

Purpose:
    Creates and tests SQLAlchemy database connections
    to PostgreSQL

Description:
    This module retrieves and validates database configuration
    from the environment, creates a SQLAlchemy Engine using the
    PostgreSQL psycopg driver, and provides a function to verify
    that the database connection is working correctly.

Functions:
    create_db_engine():
        Creates and returns a configured SQLAlchemy Engine.
    
    test_connection(engine):
        Executes a simple test query to verify database connectivity.

    get_database_version(engine):
        Retrieves the version information of the connected PostgreSQL database.

    get_schemas(engine):
        Retrieves the project's staging, warehouse, and quality schemas.
    
        get_project_tables(engine):
            Retrieves the tables belonging to the project's schemas.

Connection:
    The database connection URL is built using the following configuration:
        - DATABASE_HOST
        - DATABASE_PORT
        - DATABASE_NAME
        - DATABASE_USER
        - DATABASE_PASSWORD

Engine Configuration:
    pool_pre_ping=True is enabled to check that pooled connections
    are still valid before using them.

Dependencies:
    - SQLAlchemy
    - PostgreSQL
    - psycopg
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .config import (
    get_database_config,
    validate_database_config,
)

def create_db_engine() -> Engine:
    """
    Create and return a SQLAlchemy engine
    for the PostgreSQL database.

    Returns:
        Engine: Configured SQLAlchemy database engine.
    
    Raises:
        ValueError: If required database configuration
        is missing.
    """
    config = get_database_config()

    validate_database_config(config)

    connection_url = (
        f"postgresql+psycopg://"
        f"{config.user}:{config.password}"
        f"@{config.host}:{config.port}"
        f"/{config.database}"
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True,
    )

def test_connection(engine: Engine) -> bool:
    """
    Text whether the database connection is working.

    Args:
        engine (Engine): SQLAlchemy engine to test.
    
    Returns:
        bool: True if the database responds successfully
        to SELECT 1
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar() == 1 

def get_database_version(engine: Engine) -> str:
    """
    Retrieve the version of the connected PostgreSQL database.

    Args:
        engine (Engine):
            SQLAlchemy engine used to connect to the database.
    
    Returns:
        str: PostgreSQL server version information.        
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        return result.scalar_one()

def get_schemas(engine: Engine) -> list[str]:
    """
    Retrieve the project schemas available in the database.

    Searches the database for the 'staging', 'warehouse', and 'quality' schemas
    and returns their names in alphabetical order.

    Args:
        engine (Engine):
            SQLAlchemy engine used to query the database.
    
    Returns:
        list[str]: Names of the project schemas found in the database.
    """
    query = text("""
        SELECT schema_name FROM information_schema.schemata
        WHERE schema_name IN ('staging', 'warehouse', 'quality')
        ORDER BY schema_name;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        return [row[0] for row in result]

def get_project_tables(engine: Engine) -> list[tuple[str, str]]:
    """
    Retrieves tables belonging to the project schemas.

    Searches the 'staging', 'warehouse', and 'quality' schemas and returns
    each tables schema name and table name, ordered by schema and table.

    Args:
        engine(Engine):
            SQLAlchemy engine used to query the database.
    
    Returns:
        list[tuple[str, str]]:
            List of '(schema_name, table_name)' pairs.
    """
    query = text("""
        SELECT table_schema, table_name FROM information_schema.tables
        WHERE table_schema IN ('staging', 'warehouse', 'quality')
        ORDER BY table_schema, table_name;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        return [(row[0], row[1]) for row in result]