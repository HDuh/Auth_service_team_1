import redis
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from application.core import Config

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
app.config.from_object(Config)
marshmallow = Marshmallow(app)
db = SQLAlchemy(app)

api = Api(app)
docs = FlaskApiSpec(app)

jwt = JWTManager(app)
cache = redis.Redis(
    host=Config.CACHE_HOST,
    port=Config.CACHE_PORT,
    db=0,
    decode_responses=True
)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
