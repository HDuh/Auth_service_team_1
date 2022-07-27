from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from application.core import Config

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config.from_object(Config)


def on_startup():
    init_api()
    db.init_app(app)
    db.create_all()


def init_api():
    from api.v1.auth.routes import bp_auth
    from api.v1.role.routes import bp_role
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_role)


if __name__ == '__main__':
    on_startup()
    app.run(debug=True, host='0.0.0.0', port=5001)
