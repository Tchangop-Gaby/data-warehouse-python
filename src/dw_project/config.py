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
    return DatabaseConfig(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=int(os.getenv("DATABASE_PORT", "5432")),
        database=os.getenv("DATABASE_NAME", ""),
        user=os.getenv("DATABASE_USER", ""),
        password=os.getenv("DATABASE_PASSWORD", ""),
    ) 

def validate_database_config(config: DatabaseConfig) -> None:
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

    if missing_fields:
        raise ValueError(f"Missing required database configuration: {','.join(missing_fields)}")
