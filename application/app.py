from application.core import swagger
from application.extensions import app, db, docs, migrate
from application.commands import fill_db, create_user


def init_cli_commands(flask_app):
    flask_app.cli.add_command(fill_db)
    flask_app.cli.add_command(create_user)


def init_api(flask_app):
    from api.v1.auth.routes import bp_auth
    from api.v1.role.routes import bp_role

    flask_app.register_blueprint(bp_auth)
    flask_app.register_blueprint(bp_role)
    swagger.registration(docs)


def create_app(flask_app):
    db.init_app(flask_app)
    migrate.init_app(app, db)
    db.create_all()
    init_api(flask_app)
    init_cli_commands(app)

    return flask_app


if __name__ == '__main__':
    app = create_app(app)
    app.run(debug=True, host='0.0.0.0', port=5001)
