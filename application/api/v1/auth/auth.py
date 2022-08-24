from http import HTTPStatus

from flask import request
from flask_apispec import doc, marshal_with, MethodResource, use_kwargs
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from application.core import PROJECT_CONFIG, AUTHORIZATION_HEADER
from application.extensions import db, cache
from application.models import User, AuthHistory, Profile, Role
from application.models.models_enums import ActionsEnum
from application.schemas import LoginSchema, SignUpSchema, ChangeDataSchema
from application.schemas.responses_schemas import ResponseSchema
from application.services import change_login, change_password, change_users_credentials, expired_time
from application.utils.decorators import validate_form


class Login(MethodResource, Resource):
    """Аутентификация пользователя"""

    @doc(tags=['Auth'],
         description='User login to account',
         summary='User authentication')
    @use_kwargs(LoginSchema, location='json', apply=False)
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @validate_form(LoginSchema)
    def post(self):
        body = request.get_json()
        user = User.query.filter_by(email=body['email']).first()

        if user and check_password_hash(user.password, body['password']):
            access_token = create_access_token(
                identity={'user_id': str(user.id), 'roles': [role.role_name for role in user.role]},
                fresh=True
            )
            refresh_token = create_refresh_token(identity=str(user.id))

            history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
            db.session.add(history)
            db.session.commit()

            return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

        return {'message': 'Incorrect login or password'}, HTTPStatus.BAD_REQUEST


class SignUp(MethodResource, Resource):
    """Регистрация пользователя"""

    @doc(
        tags=['Auth'],
        description='User signup method and create account',
        summary='User registration'
    )
    @use_kwargs(SignUpSchema, location='json', apply=False)
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @validate_form(SignUpSchema)
    def post(self):
        body = request.get_json()
        email = body['email']
        user = User.query.filter_by(email=email).first()

        if not user:
            new_user = User(email=email, password=generate_password_hash(body['password']), is_active=True)
            profile = Profile(user=new_user)
            history = AuthHistory(user=new_user, user_agent=request.user_agent.string, action=ActionsEnum.SIGNUP)

            db.session.add_all([new_user, profile, history])
            # дефолтная роль
            role = Role.query.filter_by(role_name=PROJECT_CONFIG.DEFAULT_ROLES).first()

            new_user.role.append(role)
            db.session.commit()

            return {'message': f'User {new_user.email} successfully registered'}, HTTPStatus.OK

        return {'message': f'User {email} already exist'}, HTTPStatus.OK


class Logout(MethodResource, Resource):
    """Выход пользователя из УЗ"""

    @doc(
        tags=['Auth'],
        description='User logout method from account.',
        summary='User logout',
        params=AUTHORIZATION_HEADER,
    )
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @jwt_required(fresh=True)
    def post(self):
        jwt_info = get_jwt()
        cache.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify.get('user_id')).first()
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGOUT)
        db.session.add(history),
        db.session.commit()

        return {'message': 'Successfully logged out'}, HTTPStatus.OK


class Refresh(MethodResource, Resource):
    """Получение новой пары токенов в обмен на refresh"""

    @doc(
        tags=['Auth'],
        description='Generate new tokens pair exchange for refresh key',
        summary='User refresh tokens pair',
        params=AUTHORIZATION_HEADER,
    )
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @jwt_required(refresh=True)
    def post(self):
        jwt_info = get_jwt()
        cache.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

        identify = get_jwt_identity()

        user = User.query.filter_by(id=identify).first()
        access_token = create_access_token(
            identity={'user_id': str(user.id), 'roles': [role.role_name for role in user.role]},
            fresh=True
        )
        refresh_token = create_refresh_token(identity=identify)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class ChangeCredentials(MethodResource, Resource):
    """Смена логина (email) или пароля"""

    @doc(
        tags=['Auth'],
        description='Change of login (email) or/and password for user',
        summary='User change credentials',
        params=AUTHORIZATION_HEADER,
    )
    @use_kwargs(ChangeDataSchema, location='json', apply=False)
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @validate_form(ChangeDataSchema)
    @jwt_required(fresh=True)
    def post(self):
        body = request.get_json()
        email = body['email']
        old_password = body['old_password']
        new_password = body.get('new_password')
        new_password2 = body.get('new_password2')

        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify.get('user_id')).first()
        if user and str(user.id) == identify.get('user_id'):
            if (
                    email
                    and check_password_hash(user.password, old_password)
                    and not new_password
            ):
                return change_login(db, user, body)

            elif (
                    not email
                    and check_password_hash(user.password, old_password)
                    and all(itm for itm in (new_password, new_password2))
            ):
                return change_password(db, user, body)

            else:
                return change_users_credentials(db, user, body)

        return {'message': 'User not found in database'}, HTTPStatus.OK
