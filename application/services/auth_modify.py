from http import HTTPStatus

from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from application.extensions import db
from application.forms.auth_forms import ChangeDataForm
from application.models import User, AuthHistory
from application.models.models_enums import ActionsEnum

__all__ = (
    'change_login',
    'change_password',
    'change_login_and_password',
)


def change_login(user: User, form: ChangeDataForm) -> jsonify:
    """Логика смены логина (email)"""

    if not User.query.filter_by(email=form.email.data).first():
        user.email = form.email.data
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_LOGIN)

        db.session.add(history)
        db.session.commit()

        return jsonify({'message': 'Login change successfully'}, HTTPStatus.OK)

    return jsonify({'error': 'Login already exist'}, HTTPStatus.BAD_REQUEST)


def change_password(user: User, form: ChangeDataForm) -> jsonify:
    """Логика смены пароля"""

    if not check_password_hash(user.password, form.new_password.data):
        user.password = generate_password_hash(form.new_password.data)
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_PASSWORD)

        db.session.add(history)
        db.session.commit()

        return jsonify({'message': 'Password change successfully'}, HTTPStatus.OK)

    return jsonify({'message': {'Incorrect data'}}, HTTPStatus.BAD_REQUEST)


def change_login_and_password(user: User, form: ChangeDataForm) -> jsonify:
    """Логика смены логина (email) и пароля"""

    if not User.query.filter_by(email=form.email.data).first():
        user.email = form.email.data
        user.password = generate_password_hash(form.new_password.data)
        history = [
            AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_LOGIN),
            AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_PASSWORD),
        ]

        db.session.add_all(history)
        db.session.commit()

        return jsonify({'message': 'Login and password change successfully'}, HTTPStatus.OK)

    return jsonify({'error': 'Incorrect login or password'}, HTTPStatus.BAD_REQUEST)
