from http import HTTPStatus
from uuid import uuid4

from flask_restful import abort
from sqlalchemy.dialects.postgresql import insert

from models import Permission, Role


def set_permissions(db, role, permissions):
    role.role = [
        Permission(permission_name=permission) for permission in permissions
    ]
    db.session.commit()


def init_permissions(db, config):
    base_role_permissions = [(uuid4(), permission) for permission in config.BASE_PERMISSIONS]
    statement = insert(Permission).values(base_role_permissions).on_conflict_do_nothing()
    db.session.execute(statement)
    db.session.commit()


def init_default_role(db, config, permissions=None):
    if permissions is None:
        permissions = ['base_content', 'likes', 'comments']
    role_name = config.DEFAULT_ROLE
    role = Role.query.filter_by(role_name=role_name).first()

    if not role:
        default_role = ((uuid4()), role_name)
        statement = insert(Role).values(default_role).on_conflict_do_nothing()
        db.session.execute(statement)

        role = Role.query.filter_by(role_name=role_name).first()
        add_permissions(user_permissions=permissions, role=role)
        db.session.commit()


def is_user_permissions_exist(user_permissions, permissions):
    for permission in user_permissions:
        if permission not in permissions:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'Permission {permission} does not exist')


def add_permissions(user_permissions, role):
    for permission in user_permissions:
        role.permission.append(Permission.query.filter_by(permission_name=permission).first())
