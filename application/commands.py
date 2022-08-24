import click
from flask_cli import with_appcontext
from sqlalchemy.exc import ProgrammingError

from application.core import PROJECT_CONFIG
from application.extensions import db, app
from application.services import create_root


@app.cli.command("create-root")
@click.argument("password")
@with_appcontext
def create_user(password):
    """Create root user"""
    create_root(db, password)


@app.cli.command("fill-db")
def fill_db():
    """Add to DB starting permissions and roles """
    try:
        from application.services.permissions import init_permissions, init_default_roles

        init_permissions(db, PROJECT_CONFIG)
        init_default_roles(db, PROJECT_CONFIG)

    except ProgrammingError:
        raise 'Make >> flask db upgrade << command first'
