import os

from dotenv import load_dotenv

load_dotenv()

__all__ = (
    'Config',
)


class Config:
    DB: str = os.getenv('DB', 'postgresql')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_NAME: str = os.getenv('DB_NAME', 'test_database.db')
    # SQLALCHEMY_DATABASE_URI: str = f'{DB}+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{DB_NAME}"
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'catch_me_if_you_can')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_HOST: str = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT: int = int(os.getenv('FLASK_PORT', 5000))
    WTF_CSRF_ENABLED = False