from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from app.core.config import Config
from db.db import pg_db

app = Flask(__name__)
api = Api(app=app)

app.config['SQLALCHEMY_DATABASE_URI']: str = Config.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']: bool = False

swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Auth service",
            "version": "1.0",
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
    },
)

pg_db.init_app(app=app)


def main(flask_app):
    from api.v1.auth import bp_auth
    from api.v1.role import bp_role
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_role)
    flask_app.run(debug=True, host='0.0.0.0', port=5001)


if __name__ == '__main__':
    main(app)
