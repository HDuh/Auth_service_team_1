from http import HTTPStatus
from uuid import UUID

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from application.models import User


class UserProfile(Resource):
    @jwt_required(fresh=True)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user and user.id == UUID(get_jwt_identity()):
            return {'profile_id': user.profile.id,
                    'user_id': user.profile.user_id,
                    'user_email': user.email,
                    'first_name': user.profile.first_name,
                    'last_name': user.profile.last_name,
                    'age': user.profile.age,
                    'country': user.profile.country}, HTTPStatus.OK

        return {'message': f'User id {user_id} not found'}, HTTPStatus.NOT_FOUND


class UserAuthHistory(Resource):
    @jwt_required(fresh=True)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user and user.id == UUID(get_jwt_identity()):
            return [{'user_id': data.user_id,
                     'user_agent': data.user_agent,
                     'action_time': data.action_time,
                     'action': data.action.value} for data in user.auth_history.all()
                    ], HTTPStatus.OK
