from http import HTTPStatus

from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, AuthHistory, Profile, Role
from models.models_enums import ActionsEnum

__all__ = (
    'change_login',
    'change_password',
    'change_users_credentials',
    'create_root',
)


def change_login(db, user: User, body: dict):
    """Логика смены логина (email)"""

    if not User.query.filter_by(email=body['email']).first():
        user.email = body['email']
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_LOGIN)

        db.session.add(history)
        db.session.commit()

        return {'message': 'Login change successfully'}, HTTPStatus.OK

    return {'message': 'Login already exist'}, HTTPStatus.BAD_REQUEST


def change_password(db, user: User, body: dict):
    """Логика смены пароля"""
    if not check_password_hash(user.password, body['new_password']):
        user.password = generate_password_hash(body['new_password'])
        history = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_PASSWORD)

        db.session.add(history)
        db.session.commit()

        return {'message': 'Password change successfully'}, HTTPStatus.OK

    return {'message': 'Incorrect data'}, HTTPStatus.BAD_REQUEST


def change_users_credentials(db, user: User, body: dict):
    """Логика смены логина (email) и пароля"""

    if User.query.filter_by(email=body['email']).first():
        return {'message': 'Login already exist'}, HTTPStatus.BAD_REQUEST

    elif not check_password_hash(user.password, body['old_password']):
        return {'message': 'Incorrect old password'}, HTTPStatus.BAD_REQUEST

    else:
        user.email = body['email']
        user.password = generate_password_hash(body['new_password'])
        history = [
            AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_LOGIN),
            AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.CHANGE_PASSWORD),
        ]

        db.session.add_all(history)
        db.session.commit()

        return {'message': 'Login and password change successfully'}, HTTPStatus.OK


def create_root(db, password):
    user = User(email='root', password=generate_password_hash(password), is_active=True)
    profile = Profile(user=user)
    db.session.add_all([user, profile])
    # Назначаем все роли
    roles = Role.query.all()
    for role in roles:
        user.role.append(role)

    db.session.commit()
