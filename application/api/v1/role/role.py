from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from application.extensions import db
from application.forms import RoleForm, UpdateRoleForm
from application.models import Role
from application.utils.decorators import validate_form


class Roles(Resource):
    @jwt_required(fresh=True)
    @validate_form(RoleForm)
    def post(self):
        form = RoleForm()
        role = Role.query.filter_by(role_name=form.role_name.data).first()

        if role:
            return jsonify({'message': f'User {form.role_name.data} already exist'}, HTTPStatus.OK, )

        new_role = Role(role_name=form.role_name.data)
        db.session.add(new_role)
        db.session.commit()

        return jsonify({'message': f'Role {new_role.role_name} created'}, HTTPStatus.OK, )

    # @jwt_required(fresh=True)
    @validate_form(UpdateRoleForm)
    def patch(self):
        form = UpdateRoleForm()
        role = Role.query.filter(
            (Role.role_name == form.role_name.data) |
            (Role.role_name == form.new_role_name.data)
        )

        if len(role.all()) == 1 and (role := role.first()):
            role.role_name = form.new_role_name.data
            db.session.commit()
            return jsonify({'message': f'Role updated'}, HTTPStatus.OK, )

        return jsonify({'message': f'Role not found or already exist'}, HTTPStatus.NOT_MODIFIED, )

    @jwt_required(fresh=True)
    @validate_form(RoleForm)
    def delete(self):
        form = RoleForm()
        role = Role.query.filter_by(role_name=form.role_name.data)

        if role.first():
            role.delete()
            db.session.commit()
            return jsonify({'message': f'Role deleted'}, HTTPStatus.OK, )

        return jsonify({'message': f'Role not found'}, HTTPStatus.NOT_MODIFIED, )


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
