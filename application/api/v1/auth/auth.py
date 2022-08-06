from http import HTTPStatus

from flask import request
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
from application.models import User, AuthHistory, Profile, Role
from application.models.models_enums import ActionsEnum
from application.services import change_login, change_password, change_login_and_password, expired_time
from application.utils.decorators import validate_form


class Login(Resource):
    """Аутентификация пользователя"""

    @validate_form(LoginForm)
    def post(self):
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


class SignUp(Resource):
    """Регистрация пользователя"""

    @validate_form(SignUpForm)
    def post(self):
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


class Logout(Resource):
    """Выход пользователя из УЗ"""

    @jwt_required()
    def post(self):
        jwt_info = get_jwt()
        cache.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify).first()
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGOUT)
        db.session.add(history),
        db.session.commit()

        return {'message': 'Successfully logged out'}, HTTPStatus.OK


class Refresh(Resource):
    """Получение новой пары токенов в обмен на refresh"""

    @jwt_required(refresh=True)
    def post(self):
        jwt_info = get_jwt()
        cache.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

        identify = get_jwt_identity()
        access_token = create_access_token(identity=identify, fresh=True)
        refresh_token = create_refresh_token(identity=identify)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class ChangeLoginPassword(Resource):
    """Смена логина (email) или пароля"""

    @validate_form(ChangeDataForm)
    @jwt_required(fresh=True)
    def post(self):
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
                return change_login_and_password(db, user, body)

        return {'message': 'User not found in database'}, HTTPStatus.OK
