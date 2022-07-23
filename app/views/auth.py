from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from app.forms import LoginForm, SignUpForm
from app.models import User
from app.core.db import db

auth = Blueprint('auth', __name__)


class Login(Resource):
    @staticmethod
    def post():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user or not check_password_hash(user.password, form.password.data):
                return jsonify({'error': 'incorrect login or password'})
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        return jsonify({'error': 'incorrect login or password'})


class SignUp(Resource):
    @staticmethod
    def post():
        form = SignUpForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                return jsonify({'error': f'user {user.email} already exist'})
            if form.password.data == form.password2.data:
                email = form.email.data
                hashed_password = generate_password_hash(form.password.data)
                new_user = User(email=email, password=hashed_password)
                # TODO: подумать над реализацией методов общения с БД. Кастонуть менеджера, либо через миксины
                db.session.add(new_user)
                db.session.commit()
                return jsonify(email=email)
        return jsonify({'error': 'incorrect login or password'})


class Logout(Resource):
    def post(self):
        return {'logout': 1}
