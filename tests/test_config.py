"""
Database Configuration Creation Test
====================================

Purpose:
    Verify that the DatabaseConfig class correctly create 
    and stores database connection settings.

Description:
    This test creates a DatabaseConfig instance with sample
    PostgreSQL connection parametersand verifies that the 
    expected configuration values are stored correctly.

Parameters:
    host:
        Database server hostname or IP address.
    port:
        Port used by the database server.
    database:
        Name of the database to connect to.
    user:
        Username used for database authentification.

Returns:
    None. The test passes when all assertions succeed.

Dependencies:
    DatabaseConfig:
        Configuration class imported from dw_project.config.
"""
from dw_project.config import DatabaseConfig

def test_database_config_creation():
    """
    Verify that DatabaseConfig stores the provided
    configuration values.
    """
    config = DatabaseConfig(
        host="localhost",
        port=5432,
        database="test_db",
        user="postgres",
        password="secret",
    )

    # Verify that the configuration values were stored correctly.
    assert config.host == "localhost"
    assert config.port == 5432
    assert config.database == "test_db"