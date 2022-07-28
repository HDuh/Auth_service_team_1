from flask_restful import Resource


class CreateRole(Resource):
    def post(self):
        pass


class Role(Resource):
    def get(self, role_id):
        pass

    def patch(self, role_id):
        pass

    def delete(self, role_id: str):
        pass


class RoleList(Resource):
    def get(self) -> dict:
        pass


class UserRole(Resource):
    def post(self):
        pass

    def delete(self):
        pass
