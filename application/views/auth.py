from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from application.core import db
from application.forms import LoginForm, SignUpForm
from application.models import User, Profile, AuthHistory

__all__ = (
    'Login',
    'SignUp',
    'Logout',
)

from application.models.models_enums import ActionsEnum


class Login(Resource):
    @staticmethod
    def post():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if not user or not check_password_hash(user.password, form.password.data):
                return jsonify({'message': 'Incorrect login or password'}, 400, )

            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.login.value)
            db.session.add(history)
            db.session.commit()

            return jsonify(access_token=access_token, refresh_token=refresh_token)

        return jsonify({'message': 'Incorrect login or password'}, 400, )


class SignUp(Resource):
    @staticmethod
    def post():
        form = SignUpForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user:
                return jsonify({'message': f'User {form.email.data} already exist'}, 200, )

            new_user = User(email=form.email.data, password=generate_password_hash(form.password.data))
            profile = Profile(user=new_user)
            history = AuthHistory(user=new_user, user_agent=request.user_agent.string, action=ActionsEnum.signup.value)

            db.session.add_all([new_user, profile, history])
            db.session.commit()

            return jsonify({'message': f'User {new_user.email} successfully registered'}, 200, )

        return jsonify({'message': 'Incorrect login or password'}, 400, )


class Logout(Resource):
    def post(self):
        return {'logout': 1}
