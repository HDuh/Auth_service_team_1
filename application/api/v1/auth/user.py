from http import HTTPStatus
from uuid import UUID

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from application.forms.auth_forms import ChangeDataForm
from application.main import db
from application.models import User
from werkzeug.security import generate_password_hash, check_password_hash


class UserProfile(Resource):
    @jwt_required(fresh=True)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user and user.id == UUID(get_jwt_identity()):
            return jsonify(
                {
                    'profile_id': user.profile.id,
                    'user_id': user.profile.user_id,
                    'user_email': user.email,
                    'first_name': user.profile.first_name,
                    'last_name': user.profile.last_name,
                    'age': user.profile.age,
                    'country': user.profile.country,
                },
                HTTPStatus.OK,
            )

        return jsonify({'message': f'User id {user_id} not found'}, HTTPStatus.NOT_FOUND, )


class UserAuthHistory(Resource):
    @jwt_required(fresh=True)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user and user.id == UUID(get_jwt_identity()):
            return jsonify(
                [
                    {
                        'user_id': data.user_id,
                        'user_agent': data.user_agent,
                        'action_time': data.action_time,
                        'action': data.action.value,
                    }
                    for data in user.auth_history.all()
                ],
                HTTPStatus.OK,
            )


class ChangeLoginOrPassword:
    @jwt_required(fresh=True)
    def post(self):
        identify = get_jwt_identity()
        user = User.query.filter_by(id=identify).first()
        if user:
            form = ChangeDataForm()
            if form.validate_on_submit():
                if form.email and not form.new_password:
                    return change_email(user, form)
                elif not form.email and form.new_password:
                    return change_password(user, form)
                else:
                    return change_all_auth_data(user, form)


def change_email(user, form):
    if not User.query.filter_by(email=form.email).first():
        user.email = form.email
        db.session.merge(user)
        db.session.commit()
        return jsonify(
            {
                "message": "Email change successfully"
            },
            HTTPStatus.OK
        )
    else:
        return jsonify(
            {
                "error": f"Email {form.email} already exist"
            },
            HTTPStatus.BAD_REQUEST
        )


def change_password(user, form):
    if form.new_password != form.old_password and check_password_hash(user.password, form.new_password):
        user.password = generate_password_hash(form.new_password)
        db.session.merge(user)
        db.session.commit()
        return jsonify(
            {
                "message": "Password change successfully"
            },
            HTTPStatus.OK
        )
    else:
        return jsonify(
            {
                'error': "Incorrect new password"
            },
            HTTPStatus.BAD_REQUEST
        )


def change_all_auth_data(user, form):
    if (
            not User.query.filter_by(email=form.email).first()
            and form.new_password != form.old_password
            and check_password_hash(user.password, form.new_password)
    ):
        user.email = form.email.data
        user.password = generate_password_hash(form.new_password)
        db.session.merge(user)
        db.session.commit()
        return jsonify(
            {
                "message": "Email and password change successfully"
            },
            HTTPStatus.OK
        )
    return jsonify(
        {
            "error": "Incorrect email or password"
        },
        HTTPStatus.BAD_REQUEST
    )
