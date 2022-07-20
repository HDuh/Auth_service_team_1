import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'POSTGRES_CONFIG',
    'TEST_SQLITE_DB_CONFIG',
)

load_dotenv()


# class Config:
#     DB: str = os.getenv('DB', 'postgresql')
#     DB_USER: str = os.getenv('DB_USER')
#     DB_PASSWORD: str = os.getenv('DB_PASSWORD')
#     DB_HOST: str = os.getenv('DB_HOST')
#     DB_PORT: int = int(os.getenv('DB_PORT', 5432))
#     DB_NAME: str = os.getenv('DB_NAME', 'temp_database.db')
#     # SQLALCHEMY_DATABASE_URI: str = f'{DB}+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
#     SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{DB_NAME}"
#
#     FLASK_HOST: str = os.getenv('FLASK_HOST', '0.0.0.0')
#     FLASK_PORT: int = int(os.getenv('FLASK_PORT', 5001))


class PostgresSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_NAME')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')


POSTGRES_CONFIG = PostgresSettings().dict()
TEST_SQLITE_DB_CONFIG = f"sqlite:///{os.getenv('TEST_DB_NAME')}"
