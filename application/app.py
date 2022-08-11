import click
from flask_cli import with_appcontext

from core import Config, swagger
from extensions import app, db, docs
from services.auth import create_root


@app.cli.command("create-root")
@click.argument("password")
@with_appcontext
def create_user(password):
    """Create root user"""
    create_root(db, password)


def init_api(flask_app):
    from api.v1.auth.routes import bp_auth
    from api.v1.role.routes import bp_role

    flask_app.register_blueprint(bp_auth)
    flask_app.register_blueprint(bp_role)
    swagger.registration(docs)


def create_app(flask_app):
    db.init_app(flask_app)
    init_api(flask_app)
    db.create_all()
    from services.permissions import init_permissions, init_default_roles

    init_permissions(db, Config)
    init_default_roles(db, Config)

    return flask_app


if __name__ == '__main__':
    app = create_app(app)
    app.run(debug=True, host='0.0.0.0', port=5001)
