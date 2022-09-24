import redis
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from authlib.integrations.flask_client import OAuth
from flask import Flask, request
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from jaeger_client import Config
from flask_opentracing import FlaskTracer

from core import PROJECT_CONFIG, GoogleClient, YandexClient, MailClient

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
providers = {
    'google': oauth.register(**GoogleClient().dict()),
    'yandex': oauth.register(**YandexClient().dict()),
    'mail': oauth.register(**MailClient().dict()),
}


# @app.before_request
# def before_request():
#     request_id = request.headers.get('X-Request-Id')
#     if not request_id:
#         raise RuntimeError('request id is required')


def initialize_tracer():
    """ Tracing setup method """
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
        },
        service_name='auth-service')
    return config.initialize_tracer()


flaskTracer = FlaskTracer(lambda: initialize_tracer(), True, app)
