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
    