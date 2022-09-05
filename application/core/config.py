from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'PROJECT_CONFIG',
    'AUTHORIZATION_HEADER',
    'GOOGLE_CONFIG',
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

    # OAUTHLIB_INSECURE_TRANSPORT = 1
    # OAUTHLIB_RELAX_TOKEN_SCOPE = 1

    class Config:
        case_sensitive = True


@lru_cache()
class GoogleClient(BaseSettings):
    name: str = Field('google')
    client_id: str = Field(..., env='GOOGLE_CLIENT_ID')
    client_secret: str = Field(..., env='GOOGLE_CLIENT_SECRET')
    server_metadata_url: Any = Field(default='https://accounts.google.com/.well-known/openid-configuration'),
    access_token_url: Any = Field(default='https://oauth2.googleapis.com/token'),
    access_token_params: Any = Field(default=None),
    authorize_url: Any = Field(default="https://accounts.google.com/o/oauth2/auth"),
    authorize_params: Any = Field(default=None),
    client_kwargs: dict = Field(
        {
            'scope': 'openid email profile'
        }
    )


PROJECT_CONFIG = ProjectSettings()
GOOGLE_CONFIG = GoogleClient()

AUTHORIZATION_HEADER = {
    'Authorization': {
        'description':
            'Authorization HTTP header with JWT token. Like: "Bearer {token}"',
        'in': 'header',
        'type': 'string',
        'required': True,
    },
}
