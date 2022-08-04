import json
from http import HTTPStatus
from uuid import uuid4

from flask_restful import abort
from sqlalchemy.dialects.postgresql import insert

from application.models import Permission, Role


def set_permissions(db, role, permissions):
    role.role = [
        Permission(permission_name=permission) for permission in permissions
    ]
    db.session.commit()


def cache_access_roles(db, cache):
    for role in db.session.query(Role).all():
        cache.set(f'role:{role.role_name}', json.dumps([permission.permission_name for permission in role.role]))


def cache_permissions(db, cache):
    cache.set(
        'permissions',
        json.dumps([permission.permission_name for permission in db.session.query(Permission).all()])
    )


def init_permissions(db, config):
    base_role_permissions = [(uuid4(), permission) for permission in config.BASE_PERMISSIONS]
    statement = insert(Permission).values(base_role_permissions).on_conflict_do_nothing()
    db.session.execute(statement)
    db.session.commit()


def is_user_permissions_exist(user_permissions, permissions):
    for permission in user_permissions:
        if permission not in permissions:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'Permission {permission} does not exist')


def add_permissions(user_permissions, role):
    for permission in user_permissions:
        role.permission.append(Permission.query.filter_by(permission_name=permission).first())


def cache_db(db, cache):
    from application.services.permissions import cache_access_roles, cache_permissions
    cache_access_roles(db, cache)
    cache_permissions(db, cache)
