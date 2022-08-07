from http import HTTPStatus

from flask import request
from flask_apispec import doc, use_kwargs, marshal_with, MethodResource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from application.core import Config
from application.extensions import db, cache
from application.forms import LoginForm, SignUpForm, ChangeDataForm
from application.forms.responses_forms import ResponseSchema
from application.models import User, AuthHistory, Profile, Role
from application.models.models_enums import ActionsEnum
from application.services import change_login, change_password, change_users_credentials, expired_time
from application.utils.decorators import validate_form


class Login(MethodResource, Resource):
    """Аутентификация пользователя"""

    @doc(tags=['Auth'],
         description='User login to account',
         summary='User authentication')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(LoginForm)
    @validate_form(LoginForm)
    def post(self, **kwargs):
        body = request.json
        user = User.query.filter_by(email=body['email']).first()

        if user and check_password_hash(user.password, body['password']):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))

            history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
            db.session.add(history)
            db.session.commit()

            return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

        return {'message': 'Incorrect login or password'}, HTTPStatus.BAD_REQUEST


class SignUp(MethodResource, Resource):
    """Регистрация пользователя"""

    @doc(tags=['Auth'],
         description='User signup method and create account',
         summary='User registration')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(SignUpForm)
    @validate_form(SignUpForm)
    def post(self, **kwargs):
        body = request.json
        email = body['email']
        user = User.query.filter_by(email=email).first()

        if not user:
            new_user = User(email=email, password=generate_password_hash(body['password']), is_active=True)
            profile = Profile(user=new_user)
            history = AuthHistory(user=new_user, user_agent=request.user_agent.string, action=ActionsEnum.SIGNUP)

            db.session.add_all([new_user, profile, history])
            # дефолтная роль
            role = Role.query.filter_by(role_name=Config.DEFAULT_ROLE).first()

            new_user.role.append(role)
            db.session.commit()

            return {'message': f'User {new_user.email} successfully registered'}, HTTPStatus.OK

        return {'message': f'User {email} already exist'}, HTTPStatus.OK


class Logout(MethodResource, Resource):
    """Выход пользователя из УЗ"""

    @doc(tags=['Auth'], description='User logout method from account.', summary='User logout')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @jwt_required()
    def post(self, **kwargs):
        jwt_info = get_jwt()
        cache.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify).first()
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGOUT)
        db.session.add(history),
        db.session.commit()

        return {'message': 'Successfully logged out'}, HTTPStatus.OK


class Refresh(MethodResource, Resource):
    """Получение новой пары токенов в обмен на refresh"""

    @doc(tags=['Auth'],
         description='Generate new tokens pair exchange for refresh key',
         summary='User refresh tokens pair')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @jwt_required(refresh=True)
    def post(self, **kwargs):
        jwt_info = get_jwt()
        cache.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

        identify = get_jwt_identity()
        access_token = create_access_token(identity=identify, fresh=True)
        refresh_token = create_refresh_token(identity=identify)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class ChangeCredentials(MethodResource, Resource):
    """Смена логина (email) или пароля"""

    @doc(tags=['Auth'],
         description='Change of login (email) or/and password for user',
         summary='User change credentials')
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    @use_kwargs(ChangeDataForm)
    @validate_form(ChangeDataForm)
    @jwt_required(fresh=True)
    def post(self, **kwargs):
        body = request.json
        email = body['email']
        old_password = body['old_password']
        new_password = body.get('new_password')
        new_password2 = body.get('new_password2')

        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify).first()
        if user and str(user.id) == get_jwt_identity():
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
