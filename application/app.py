import click
from flask_cli import with_appcontext

from application.core import Config, swagger
from application.extensions import app, db, cache, docs
from application.services.auth import create_root


@app.cli.command("create-root")
@click.argument("password")
@with_appcontext
def create_user(password):
    """Create root user"""
    create_root(db, password)


def init_api():
    from application.api.v1.auth.routes import bp_auth
    from application.api.v1.role.routes import bp_role

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_role)
    swagger.registration(docs)


def create_app(flask_app):
    db.init_app(flask_app)
    init_api()
    db.create_all()
    from application.services.permissions import init_permissions, init_default_role

    init_permissions(db, Config)
    init_default_role(db, Config)

    return flask_app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
