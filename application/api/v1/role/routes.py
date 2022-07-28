from flask import Blueprint
from flask_restful import Api

from .role import RoleList, Roles, UserRole

bp_role = Blueprint('role', __name__)
api = Api(bp_role)

api.add_resource(RoleList, '/roles/')
api.add_resource(Roles, '/role/')
api.add_resource(UserRole, '/user_role/')
