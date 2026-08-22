from sqlalchemy import create_engine
from .config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD
)

def get_engine():
    """
    Create and return a SQLAlchemy database engine
        The engine manages connections between the 
        pipeline and the database.

    Returns:
        Engine: A SQLAlchemy Engine instance used to
        interact with the database
    """

    connection_url = (
                f"postgresql+psycopg://"
                f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
                f"{DATABASE_HOST}:{DATABASE_PORT}/"
                f"{DATABASE_NAME}"
        )

    return create_engine(connection_url)