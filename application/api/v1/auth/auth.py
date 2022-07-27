from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request,
)
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from application.core.database import db
from application.core.jwt_manager import block_list
from application.forms import LoginForm, SignUpForm
from application.models import User, AuthHistory, Profile
from application.models.models_enums import ActionsEnum


class Login(Resource):
    @staticmethod
    def post():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(user.password, form.password.data):
                access_token = create_access_token(identity=str(user.id), fresh=True)
                refresh_token = create_refresh_token(identity=str(user.id))

                history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN.value)
                db.session.add(history)
                db.session.commit()

                return jsonify(access_token=access_token, refresh_token=refresh_token)

        return jsonify({'message': 'Incorrect login or password'}, HTTPStatus.BAD_REQUEST, )


class SignUp(Resource):
    @staticmethod
    def post():
        form = SignUpForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user:
                return jsonify({'message': f'User {form.email.data} already exist'}, HTTPStatus.OK, )

            new_user = User(email=form.email.data, password=generate_password_hash(form.password.data), is_active=True)
            profile = Profile(user=new_user)
            history = AuthHistory(user=new_user, user_agent=request.user_agent.string, action=ActionsEnum.SIGNUP.value)

            db.session.add_all([new_user, profile, history])
            db.session.commit()

            return jsonify({'message': f'User {new_user.email} successfully registered'}, HTTPStatus.OK, )

        return jsonify({'message': 'Incorrect login or password'}, HTTPStatus.BAD_REQUEST, )


class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        block_list.add(jti)

        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify).first()
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGOUT.value)
        db.session.add(history),
        db.session.commit()

        return jsonify(
            {
                'message': 'Successfully logged out'
            },
            HTTPStatus.OK,
        )


class Refresh(Resource):
    """Получение новой пары токенов в обмен на refresh"""

    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        block_list.add(jti)

        identify = int(get_jwt_identity())
        access_token = create_access_token(identity=identify, fresh=True)
        refresh_token = create_refresh_token(identity=identify)
        return jsonify(
            {
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            HTTPStatus.OK,
        )


class ChangeUserPassword:
    @jwt_required(fresh=True)
    def post(self):
        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify).first()
        if user and user.id == int(get_jwt_identity()):
            ...
