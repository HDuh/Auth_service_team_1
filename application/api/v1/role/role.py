import json
from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from application.extensions import db, cache
from application.forms import RoleForm, UpdateRoleForm
from application.forms.role_forms import RoleBase, UserRoleForm
from application.models import Role, User
from application.services.permissions import is_user_permissions_exist, add_permissions
from application.utils.decorators import validate_form


class Roles(Resource):
    @validate_form(RoleForm)
    @jwt_required(fresh=True)
    def post(self):
        body = request.json
        role_name = body['role_name']
        user_permissions = body['permissions']
        role = Role.query.filter_by(role_name=role_name).first()
        permissions = json.loads(cache.get('permissions'))

        is_user_permissions_exist(user_permissions, permissions)

        if role:
            return {'message': f'Role {role_name} already exist'}, HTTPStatus.BAD_REQUEST

        new_role = Role(role_name=role_name)
        add_permissions(user_permissions, new_role)
        db.session.add(new_role)
        db.session.commit()
        cache.set(f'role:{role_name}', json.dumps(user_permissions))

        return {'message': f'Role {role_name} created'}, HTTPStatus.CREATED

    @validate_form(UpdateRoleForm)
    @jwt_required(fresh=True)
    def patch(self):
        body = request.json
        old_name = body['role_name']
        new_name = body['new_role_name']
        user_permissions = body['permissions']
        permissions = json.loads(cache.get('permissions'))

        is_user_permissions_exist(user_permissions, permissions)

        roles_query = Role.query.filter(Role.role_name.in_([old_name, new_name]))
        roles = {role.role_name for role in roles_query.all()}

        if old_name not in roles:
            return {'message': f'Role not found'}, HTTPStatus.BAD_REQUEST
        elif new_name in roles:
            return {'message': f'Role already exist'}, HTTPStatus.BAD_REQUEST

        role = roles_query.first()
        db_permissions = [db_permission.permission_name for db_permission in role.role]
        for permission in db_permissions:
            if permission in user_permissions:
                return {'message': f'Permission {permission} already exist in role {old_name}'}, HTTPStatus.BAD_REQUEST

        role.role_name = new_name
        add_permissions(user_permissions, role)
        db.session.commit()

        cache.delete(f'role:{old_name}')
        cache.set(f'role:{new_name}', json.dumps(user_permissions + db_permissions))

        return {'message': 'Role updated'}, HTTPStatus.OK

    @validate_form(RoleBase)
    @jwt_required(fresh=True)
    def delete(self):
        body = request.json
        role_name = body['role_name']
        role = Role.query.filter_by(role_name=role_name).first()

        if role:
            db.session.delete(role)
            db.session.commit()
            return {'message': f'Role {role_name} deleted'}, HTTPStatus.OK

        return {'message': f'Role {role_name} not found'}, HTTPStatus.NOT_FOUND


class RoleList(Resource):
    @jwt_required(fresh=True)
    def get(self):
        roles = []
        for cached_role in cache.scan_iter('role:*'):
            value = cache.get(cached_role)
            roles.append({cached_role.replace('role:', ''): json.loads(value)})
        return roles, HTTPStatus.OK


class UserRole(Resource):
    @validate_form(UserRoleForm)
    @jwt_required(fresh=True)
    def post(self):
        body = request.json
        email = body['email']
        role_name = body['role_name']
        user = User.query.filter_by(email=email).first()
        role = Role.query.filter_by(role_name=body['role_name']).first()

        if user and role and role not in user.role:
            user.role.append(role)
            db.session.commit()
            return {'message': f'Role {role_name} assigned to user {email}'}, HTTPStatus.OK

        return {'message': f'Role {role_name} does not assign to user {email}'}, HTTPStatus.NOT_FOUND

    @validate_form(UserRoleForm)
    @jwt_required(fresh=True)
    def delete(self):
        body = request.json
        email = body['email']
        role_name = body['role_name']
        user = User.query.filter_by(email=email).first()
        role = Role.query.filter_by(role_name=body['role_name']).first()

        if user and role and role in user.role:
            user.role.remove(role)
            db.session.commit()
            return {'message': f'Role {role_name} removed from user {email}'}, HTTPStatus.OK

        return {'message': f'Role {role_name} does not remove from user {email}'}, HTTPStatus.NOT_FOUND
