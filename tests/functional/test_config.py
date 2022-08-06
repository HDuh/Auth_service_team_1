import os

from dotenv import load_dotenv

__all__ = (
    'Config',
)

load_dotenv()


class Config:
    # postgres
    DB: str = os.getenv('DB', 'postgresql')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_NAME: str = os.getenv('DB_NAME')

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI: str = f'{DB}+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask app
    FLASK_HOST: str = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT: int = int(os.getenv('FLASK_PORT', 5000))

    # jwt
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # other
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    WTF_CSRF_ENABLED = False
    TEST_DATABASE_URI: str = f'{DB}+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/test'
    
