from flask import Flask
from flask_restful import Api

from application.core import Config

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI']: str = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']: bool = False


def init_api():
    from api.v1.auth.routes import bp_auth
    from api.v1.role.routes import bp_role
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_role)


if __name__ == '__main__':
    init_api()

    from application.core.database import init_db

    init_db()

    app.run(debug=True, host='0.0.0.0', port=5001)
