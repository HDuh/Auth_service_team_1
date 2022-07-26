from flask import Flask

from application.core import Config

app = Flask(__name__)


def create_app():
    app.config.from_object(Config)
