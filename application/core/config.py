from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'PROJECT_CONFIG',
    'AUTHORIZATION_HEADER',
    'GoogleClient',
    'YandexClient',
    'MailClient',
)
load_dotenv()


@lru_cache()
class ProjectSettings(BaseSettings):
    # postgres
    DB: str = Field(..., env='DB')
    DB_HOST: str = Field(..., env='DB_HOST')
    DB_NAME: str = Field(..., env='DB_NAME')
    DB_PASSWORD: str = Field(..., env='DB_PASSWORD')
    DB_PORT: int = Field(..., env='DB_PORT')
    DB_USER: str = Field(..., env='DB_USER')

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI: str = Field(..., env='SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool

    # flask app
    FLASK_HOST: str = Field(..., env='FLASK_HOST')
    FLASK_PORT: int = Field(..., env='FLASK_PORT')
    API_PORT: int = Field(..., env='API_PORT')

    # cache
    CACHE_HOST: str = Field(..., env='REDIS_HOST')
    CACHE_PORT: int = Field(..., env='REDIS_PORT')

    # jwt
    JWT_BLACKLIST_ENABLED: bool
    JWT_BLACKLIST_TOKEN_CHECKS: list = ['access', 'refresh']

    # other
    BASE_PERMISSIONS: list = Field(..., env='BASE_PERMISSIONS')
    BASE_ROLES: list = Field(..., env='BASE_ROLES')
    DEFAULT_ROLES: str = Field(..., env='DEFAULT_ROLES')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    WTF_CSRF_ENABLED: bool

    # tracer
    JAEGER_AGENT_HOST_NAME: str = Field(..., env='JAEGER_AGENT_HOST_NAME')
    JAEGER_AGENT_PORT: int = Field(..., env='JAEGER_AGENT_PORT')

    # limiter
    LIMITER_DB: int = Field("3", env='LIMITER_DB')

    class Config:
        case_sensitive = True


@lru_cache()
class GoogleClient(BaseSettings):
    name: str = Field('google')
    client_id: str = Field(..., env='GOOGLE_CLIENT_ID')
    client_secret: str = Field(..., env='GOOGLE_CLIENT_SECRET')
    server_metadata_url: str = Field('https://accounts.google.com/.well-known/openid-configuration')
    access_token_url: str = Field('https://oauth2.googleapis.com/token')
    authorize_url: str = Field('https://accounts.google.com/o/oauth2/auth')
    client_kwargs: dict = Field(
        {
            'scope': 'openid email profile'
        }
    )


@lru_cache()
class YandexClient(BaseSettings):
    name: str = Field('yandex')
    client_id: str = Field(..., env='YANDEX_CLIENT_ID')
    client_secret: str = Field(..., env='YANDEX_CLIENT_SECRET')
    access_token_url: str = Field('https://oauth.yandex.ru/token')
    authorize_url: str = Field('https://oauth.yandex.ru/authorize')
    userinfo_endpoint: str = Field('https://login.yandex.ru/info')


@lru_cache()
class MailClient(BaseSettings):
    name: str = Field('mail')
    client_id: str = Field(..., env='MAIL_CLIENT_ID')
    client_secret: str = Field(..., env='MAIL_CLIENT_SECRET')
    access_token_url: str = Field('https://oauth.mail.ru/token')
    authorize_url: str = Field('https://oauth.mail.ru/login')
    userinfo_endpoint: str = Field('https://oauth.mail.ru/userinfo')


PROJECT_CONFIG = ProjectSettings()

AUTHORIZATION_HEADER = {
    'Authorization': {
        'description':
            'Authorization HTTP header with JWT token. Like: "Bearer {token}"',
        'in': 'header',
        'type': 'string',
        'required': True,
    },
}
