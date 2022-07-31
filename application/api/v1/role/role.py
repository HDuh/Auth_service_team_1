from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restful import Resource

from application.extensions import db
from application.forms import RoleForm, UpdateRoleForm
from application.models import Role
from application.utils.decorators import validate_form


class Roles(Resource):
    @validate_form(RoleForm)
    @jwt_required(fresh=True)
    def post(self):
        form = RoleForm()
        role = Role.query.filter_by(role_name=form.role_name.data).first()

        if role:
            return {'message': f'Role {form.role_name.data} already exist'}, HTTPStatus.BAD_REQUEST

        new_role = Role(role_name=form.role_name.data)
        db.session.add(new_role)
        db.session.commit()

        return {'message': f'Role {new_role.role_name} created'}, HTTPStatus.CREATED

    @validate_form(RoleForm)
    @jwt_required(fresh=True)
    def patch(self):
        form = UpdateRoleForm()
        roles_query = Role.query.filter(
            (Role.role_name == form.role_name.data) |
            (Role.role_name == form.new_role_name.data)
        )
        roles = [i.role_name for i in roles_query.all()]

        old_name = form.role_name.data
        new_name = form.new_role_name.data

        if old_name not in roles:
            return {'message': f'Role not found'}, HTTPStatus.BAD_REQUEST

        elif new_name in roles:
            return {'message': f'Role already exist'}, HTTPStatus.BAD_REQUEST

        elif new_name == old_name:
            return {'message': f'Role name should be different'}, HTTPStatus.BAD_REQUEST

        else:
            roles_query.first().role_name = form.new_role_name.data
            db.session.commit()
            return {'message': 'Role updated'}, HTTPStatus.OK

    @validate_form(RoleForm)
    @jwt_required(fresh=True)
    def delete(self):
        form = RoleForm()
        role = Role.query.filter_by(role_name=form.role_name.data)

        if role.first():
            role.delete()
            db.session.commit()
            return {'message': f'Role {form.role_name.data} deleted'}, HTTPStatus.OK

        return {'message': f'Role {form.role_name.data} not found'}, HTTPStatus.NOT_FOUND


class RoleList(Resource):
    def get(self) -> dict:
        pass


class UserRole(Resource):
    @jwt_required(fresh=True)
    def post(self):
        pass

    @jwt_required(fresh=True)
    def delete(self):
        pass
