from . import api
from .role import RoleList, CreateRole, Role, UserRole

api.add_resource(RoleList, '/roles/')
api.add_resource(CreateRole, '/role/')
api.add_resource(Role, '/role/<string:role_id>')
api.add_resource(UserRole, '/user_role/')
