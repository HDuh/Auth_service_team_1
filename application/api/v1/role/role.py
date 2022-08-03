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

        if not role:
            new_role = Role(role_name=form.role_name.data)
            db.session.add(new_role)
            db.session.commit()
            return {'message': f'Role {new_role.role_name} created'}, HTTPStatus.CREATED

        return {'message': f'Role {form.role_name.data} already exist'}, HTTPStatus.BAD_REQUEST

    @validate_form(UpdateRoleForm)
    @jwt_required(fresh=True)
    def patch(self):
        form = UpdateRoleForm()

        old_name = form.role_name.data
        new_name = form.new_role_name.data

        roles_query = Role.query.filter(Role.role_name.in_([old_name, new_name]))
        roles = {role.role_name for role in roles_query.all()}

        if old_name not in roles:
            return {'message': f'Role not found'}, HTTPStatus.BAD_REQUEST

        elif new_name in roles:
            return {'message': f'Role already exist'}, HTTPStatus.BAD_REQUEST

        roles_query.first().role_name = new_name
        db.session.commit()
        return {'message': 'Role updated'}, HTTPStatus.OK

    @validate_form(RoleForm)
    @jwt_required(fresh=True)
    def delete(self):
        form = RoleForm()
        role = Role.query.filter_by(role_name=form.role_name.data).first()

        if role:
            db.session.delete(role)
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
