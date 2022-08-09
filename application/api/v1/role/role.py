from http import HTTPStatus

from flask import request
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from extensions import db
from forms import RoleForm, UpdateRoleForm
from forms.responses_forms import ResponseSchema
from forms.role_forms import RoleBase, UserRoleForm
from models import Role, User, Permission
from services.permissions import is_user_permissions_exist, add_permissions
from utils.decorators import validate_form, role_access


class Roles(MethodResource, Resource):
    """ Создание, редактирование и удаление ролей """

    @doc(tags=['Role'],
         description='Role create',
         summary='Role create')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(RoleForm)
    @validate_form(RoleForm)
    @jwt_required(fresh=True)
    @role_access('admin')
    def post(self, **kwargs):
        body = request.json
        role_name = body['role_name']
        user_permissions = body['permissions']
        role = Role.query.filter_by(role_name=role_name).first()
        permissions = [permission.permission_name for permission in Permission.query.all()]

        is_user_permissions_exist(user_permissions, permissions)

        if role:
            return {'message': f'Role {role_name} already exist'}, HTTPStatus.BAD_REQUEST

        new_role = Role(role_name=role_name)
        add_permissions(user_permissions, new_role)
        db.session.add(new_role)
        db.session.commit()

        return {'message': f'Role {role_name} created'}, HTTPStatus.CREATED

    @doc(tags=['Role'],
         description='Role changing data',
         summary='Role changing data')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(UpdateRoleForm)
    @validate_form(UpdateRoleForm)
    @jwt_required(fresh=True)
    @role_access('admin')
    def patch(self, **kwargs):
        body = request.json
        old_name = body['role_name']
        new_name = body['new_role_name']
        user_permissions = body['permissions']
        permissions = [permission.permission_name for permission in Permission.query.all()]

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

        return {'message': 'Role updated'}, HTTPStatus.OK

    @doc(tags=['Role'],
         description='Role delete',
         summary='Role delete')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(RoleBase)
    @validate_form(RoleBase)
    @jwt_required(fresh=True)
    @role_access('admin')
    def delete(self, **kwargs):
        body = request.json
        role_name = body['role_name']
        role = Role.query.filter_by(role_name=role_name).first()

        if role:
            db.session.delete(role)
            db.session.commit()
            return {'message': f'Role {role_name} deleted'}, HTTPStatus.OK

        return {'message': f'Role {role_name} not found'}, HTTPStatus.NOT_FOUND


class RoleList(MethodResource, Resource):
    """ Список всех ролей """
    @doc(tags=['Role'],
         description='All roles list',
         summary='All roles list')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @jwt_required(fresh=True)
    @role_access('admin', 'moderator')
    def get(self, **kwargs):
        return [
                   {
                       role.role_name: [permission.permission_name for permission in role.permission]
                   } for role in Role.query.all()
               ], HTTPStatus.OK


class UserRole(MethodResource, Resource):
    """ Присвоение/ удаление роли у пользователя """

    @doc(tags=['Role'],
         description='Assign role to a user',
         summary='Assign role to a user')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(UserRoleForm)
    @validate_form(UserRoleForm)
    @jwt_required(fresh=True)
    @role_access('admin', 'moderator')
    def post(self, **kwargs):
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

    @doc(tags=['Role'],
         description='Delete role from user',
         summary='Delete role from user')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(UserRoleForm)
    @validate_form(UserRoleForm)
    @jwt_required(fresh=True)
    @role_access('admin', 'moderator')
    def delete(self, **kwargs):
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
