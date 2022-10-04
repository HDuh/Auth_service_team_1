from http import HTTPStatus

from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, AuthHistory, Profile, Role, Provider
from models.models_enums import ActionsEnum
from utils.user_agent_pars import get_browser

__all__ = (
    'change_login',
    'change_password',
    'change_users_credentials',
    'create_root',
    'register_provider_user'
)


def change_login(db, user: User, body: dict):
    """Логика смены логина (email)"""

    if not User.query.filter_by(email=body['email']).first():
        user.email = body['email']
        user_agent = request.user_agent.string
        browser = get_browser(user_agent)
        history = AuthHistory(user=user, user_agent=user_agent, action=ActionsEnum.CHANGE_LOGIN, browser=browser)

        db.session.add(history)
        db.session.commit()

        return {'message': 'Login change successfully'}, HTTPStatus.OK

    return {'message': 'Login already exist'}, HTTPStatus.BAD_REQUEST


def change_password(db, user: User, body: dict):
    """Логика смены пароля"""
    if not check_password_hash(user.password, body['new_password']):
        user.password = generate_password_hash(body['new_password'])
        user_agent = request.user_agent.string
        browser = get_browser(user_agent)
        history = AuthHistory(user=user, user_agent=user_agent, action=ActionsEnum.CHANGE_PASSWORD, browser=browser)

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
        user_agent = request.user_agent.string
        browser = get_browser(user_agent)

        history = [
            AuthHistory(user=user, user_agent=user_agent, action=ActionsEnum.CHANGE_LOGIN, browser=browser),
            AuthHistory(user=user, user_agent=user_agent, action=ActionsEnum.CHANGE_PASSWORD, browser=browser),
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


def register_provider_user(email, uid, provider, request, db, role):
    user = User(
        email=email,
        password=generate_password_hash(uid),
        social_signup=True
    )
    new_provider = Provider(id=int(uid), user=user, provider_name=provider)
    user_agent = request.user_agent.string
    browser = get_browser(user_agent)

    history_signup = AuthHistory(user=user, user_agent=user_agent, action=ActionsEnum.SIGNUP, browser=browser)
    history_login = AuthHistory(user=user, user_agent=user_agent, action=ActionsEnum.LOGIN, browser=browser)
    role = Role.query.filter_by(role_name=role).first()
    user.role.append(role)
    db.session.add_all([user, new_provider, history_signup, history_login])
    return user
