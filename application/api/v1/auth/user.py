from http import HTTPStatus
from uuid import UUID

from flask_apispec import MethodResource, doc, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from core import AUTHORIZATION_HEADER
from models import User
from schemas.responses_schemas import ResponseSchema
from utils.decorators import role_access


class UserProfile(MethodResource, Resource):
    """ Профиль пользователя со всей информацией о нем """

    @doc(
        tags=['User'],
        description='User profile with full info',
        summary='User profile',
        params=AUTHORIZATION_HEADER,
    )
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=404, description='Bad server response', apply=False)
    @jwt_required(fresh=True)
    @role_access('regular_user', 'admin', 'moderator')
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user and user.id == UUID(get_jwt_identity()['user_id']):
            return {
                       'profile_id': str(user.profile.id),
                       'user_id': str(user.profile.user_id),
                       'user_email': user.email,
                       'first_name': user.profile.first_name,
                       'last_name': user.profile.last_name,
                       'age': user.profile.age,
                       'country': user.profile.country
                   }, HTTPStatus.OK

        return {'message': f'User id {user_id} not found'}, HTTPStatus.NOT_FOUND


class UserAuthHistory(MethodResource, Resource):
    """ История действий по аунтификации(вход, выход, смена пароля) пользователя """

    @doc(
        tags=['User'],
        description='History of authentication actions (login, logout, password change) of the user',
        summary='User authentication history',
        params=AUTHORIZATION_HEADER,
    )
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=404, description='Bad server response', apply=False)
    @jwt_required(fresh=True)
    @role_access('regular_user', 'admin', 'moderator')
    def get(self, user_id, page, per_page):
        user = User.query.filter_by(id=user_id).first()
        if user and user.id == UUID(get_jwt_identity()['user_id']):
            return [
                       {
                           'user_id': str(data.user_id),
                           'user_agent': data.user_agent,
                           'action_time': str(data.action_time),
                           'action': data.action.value
                       } for data in user.auth_history.paginate(page=page, per_page=per_page, max_per_page=50).items
                   ], HTTPStatus.OK

        return {'message': f'User id {user_id} not found'}, HTTPStatus.NOT_FOUND
