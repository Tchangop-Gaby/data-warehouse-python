from dw_project.config import DatabaseConfig

def test_database_config_creation():
    config = DatabaseConfig(
        host="localhost",
        port=5432,
        database="test_db",
        user="postgres",
        password="secret",
    )

    assert config.host == "localhost"
    assert config.port == 5432
    assert config.database == "test_db"