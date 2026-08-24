"""
Database Configuration
======================

Purpose:
    Loads, stores, and validates database connection
    settings from environment variables.

Description:
    This model loads database configuration from the '.env' file,
    a structured 'DatabaseConfig' object, and validates that all
    required database settings are available.

Configuration:
    DATABASE_HOST       - Database server hostname.
    DATABASE_PORT       - Database server port.
    DATABASE_NAME       - Database name.
    DATABASE_USER       - Database username.
    DATABASE_PASSWORD   - Database password.    
"""
import os 
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str

def get_database_config() -> DatabaseConfig:
    """
    Loads the database settings and returns a DatabaseConfig object.
    """

    return DatabaseConfig(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=int(os.getenv("DATABASE_PORT", "5432")),
        database=os.getenv("DATABASE_NAME", ""),
        user=os.getenv("DATABASE_USER", ""),
        password=os.getenv("DATABASE_PASSWORD", ""),
    ) 

def validate_database_config(config: DatabaseConfig) -> None:
    """
    Validates that all required databaseconfiguration
    values are provided
    """
    required_fields = {
        "DATABASE_HOST": config.host,
        "DATABASE_PORT": config.port,
        "DATABASE_NAME": config.database,
        "DATABASE_USER": config.user,
        "DATABASE_PASSWORD": config.password
    }

    missing_fields = [
        name for name, value in required_fields.items() \
        if value in ("", None)
    ]

    # Raise an exception if one or more required database confiruation values are missing.
    if missing_fields:
        raise ValueError(f"Missing required database configuration: {','.join(missing_fields)}")
