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

from application.core.jwt_blocklist import jwt_redis_blocklist
from application.extensions import db
from application.forms import LoginForm, SignUpForm, ChangeDataForm
from application.models import User, AuthHistory, Profile
from application.models.models_enums import ActionsEnum
from application.services import change_login, change_password, change_login_and_password, expired_time


class Login(Resource):
    """Аутентификация пользователя"""

    @staticmethod
    def post():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(user.password, form.password.data):
                access_token = create_access_token(identity=str(user.id), fresh=True)
                refresh_token = create_refresh_token(identity=str(user.id))

                history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
                db.session.add(history)
                db.session.commit()

                return {'access_token': access_token, 'refresh_token': refresh_token}

        return {'message': 'Incorrect login or password'}, HTTPStatus.BAD_REQUEST


class SignUp(Resource):
    """Регистрация пользователя"""

    @staticmethod
    def post():
        form = SignUpForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user:
                return {'message': f'User {form.email.data} already exist'}, HTTPStatus.OK

            new_user = User(email=form.email.data, password=generate_password_hash(form.password.data), is_active=True)
            profile = Profile(user=new_user)
            history = AuthHistory(user=new_user, user_agent=request.user_agent.string, action=ActionsEnum.SIGNUP)

            db.session.add_all([new_user, profile, history])
            db.session.commit()

            return {'message': f'User {new_user.email} successfully registered'}, HTTPStatus.OK

        return {'message': 'Incorrect login or password'}, HTTPStatus.BAD_REQUEST


class Logout(Resource):
    """Выход пользователя из УЗ"""

    @jwt_required()
    def post(self):
        jwt_info = get_jwt()
        jwt_redis_blocklist.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

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
        jwt_redis_blocklist.set(jwt_info['jti'], "", ex=expired_time(jwt_info['exp']))

        identify = get_jwt_identity()
        access_token = create_access_token(identity=identify, fresh=True)
        refresh_token = create_refresh_token(identity=identify)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class ChangeLoginPassword(Resource):
    """Смена логина (email) или пароля"""

    @jwt_required(fresh=True)
    def post(self):
        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify).first()
        if user and str(user.id) == get_jwt_identity():
            form = ChangeDataForm()
            if form.validate_on_submit():
                if (
                        form.email.data
                        and check_password_hash(user.password, form.old_password.data)
                        and not form.new_password.data
                ):
                    return change_login(user, form)

                elif (
                        not form.email.data
                        and check_password_hash(user.password, form.old_password.data)
                        and all(itm for itm in (form.new_password.data, form.new_password2.data))
                ):
                    return change_password(user, form)

                else:
                    return change_login_and_password(user, form)

            return {'error': 'Incorrect data'}, HTTPStatus.BAD_REQUEST

        return {'error': 'User not found in database'}, HTTPStatus.OK
