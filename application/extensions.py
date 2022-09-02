import redis
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from application.core import PROJECT_CONFIG

app = Flask(__name__)
app.config.from_object(PROJECT_CONFIG)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='AUTH team1 project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
docs = FlaskApiSpec(app)
jwt = JWTManager(app)
cache = redis.Redis(
    host=PROJECT_CONFIG.CACHE_HOST,
    port=PROJECT_CONFIG.CACHE_PORT,
    db=0,
    decode_responses=True
)
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="143045074071-t3u81o285uibeopphiuaibbo6kgu86no.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
