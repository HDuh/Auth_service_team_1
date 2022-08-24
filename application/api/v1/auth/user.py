from http import HTTPStatus

from flask_apispec import MethodResource, doc, marshal_with, use_kwargs
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow.fields import Int

from core import AUTHORIZATION_HEADER
from models import User
from schemas.responses_schemas import ResponseSchema, AuthHistoryResponse, UserProfileResponse
from utils.decorators import role_access


class UserProfile(MethodResource, Resource):
    """ Профиль пользователя со всей информацией о нем """

    @doc(
        tags=['User'],
        description='User profile with full info',
        summary='User profile',
        params=AUTHORIZATION_HEADER,
    )
    @marshal_with(UserProfileResponse, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=404, description='Bad server response', apply=False)
    @jwt_required(fresh=True)
    # @role_access('regular_user', 'admin', 'moderator')
    def get(self):
        user_id = get_jwt_identity().get('user_id')
        user = User.query.filter_by(id=user_id).first()

        if user and str(user.id) == user_id:
            return {
                       'profile_id': user.profile.id,
                       'user_id': user.profile.user_id,
                       'user_email': user.email,
                       'first_name': user.profile.first_name,
                       'last_name': user.profile.last_name,
                       'age': user.profile.age,
                       'country': user.profile.country
                   }, HTTPStatus.OK

        return {'message': f'User not found'}, HTTPStatus.NOT_FOUND


class UserAuthHistory(MethodResource, Resource):
    """ История действий по аунтификации(вход, выход, смена пароля) пользователя """

    @doc(
        tags=['User'],
        description='History of authentication actions (login, logout, password change) of the user',
        summary='User authentication history',
        params=AUTHORIZATION_HEADER,
    )
    @use_kwargs(
        {
            'page': Int(description='Page number'),
            'per_page': Int(description='Data on page')
        },
        location='query', apply=False
    )
    @marshal_with(AuthHistoryResponse(many=True), code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=404, description='Bad server response', apply=False)
    @jwt_required(fresh=True)
    # @role_access('regular_user', 'admin', 'moderator')
    def get(self):
        from flask import request
        input_params = request.args.to_dict()
        page, per_page = input_params.get('page'), input_params.get('per_page')
        user_id = get_jwt_identity().get('user_id')
        user = User.query.filter_by(id=user_id).first()
        if user and str(user.id) == user_id:
            result = []
            for data in user.auth_history.paginate(page=int(page) if page else None,
                                                   per_page=int(per_page) if per_page else None,
                                                   max_per_page=50).items:
                result.append(
                    {
                        'user_id': data.user_id,
                        'user_agent': data.user_agent,
                        'action_time': data.action_time.isoformat(),
                        'action': data.action.value
                    }
                )
            return result, HTTPStatus.OK

        return {'message': f'User not found'}, HTTPStatus.NOT_FOUND
