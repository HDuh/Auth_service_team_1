from http import HTTPStatus

from flask import url_for, request
from flask_apispec import doc, marshal_with
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from application.core import PROJECT_CONFIG
from application.extensions import providers, db
from application.models import Provider, User, AuthHistory, Role
from application.models.models_enums import ActionsEnum
from application.schemas.responses_schemas import ResponseSchema
from application.services import get_tokens


class SocialProvider(Resource):
    @doc(
        tags=['Social auth'],
        description='Auth through external service',
        summary='User auth'
    )
    @marshal_with(ResponseSchema, code=302, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    def get(self, provider_name: str):
        if provider_name not in providers.keys():
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'{provider_name} not supported')

        redirect_uri = url_for('auth.socialproviderauth', _external=True, provider_name=provider_name)
        return providers.get(provider_name).authorize_redirect(redirect_uri)


class GoogleProviderAuth(Resource):
    @doc(
        tags=['Google'],
        description='Auth through google',
        summary='User auth'
    )
    @marshal_with(ResponseSchema, code=302, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    def get(self):
        token = providers.get('google').authorize_access_token()
        user_info = token['userinfo']
        provider = Provider.query.filter_by(id=int(user_info['sub'])).first()
        if not provider:
            user = User(
                email=user_info['email'],
                password=generate_password_hash(user_info['sub']),
                social_signup=True
            )
            new_provider = Provider(id=int(user_info['sub']), user=user, provider_name='google')
            history_signup = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.SIGNUP)
            history_login = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
            role = Role.query.filter_by(role_name=PROJECT_CONFIG.DEFAULT_ROLES).first()
            user.role.append(role)
            db.session.add_all([user, new_provider, history_signup, history_login])
        else:
            user = provider.user
            history_login = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
            db.session.add(history_login)

        db.session.commit()
        access_token, refresh_token = get_tokens(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class YandexProviderAuth(Resource):
    @doc(
        tags=['Yandex'],
        description='Auth through yandex',
        summary='User auth'
    )
    def get(self):
        token = providers.get('yandex').authorize_access_token()
        # user_info = token['userinfo']
        # TODO: доп запрос для получения информации о пользователе
        # TODO: вынести отдельно логику добавления пользователя в бд

        return {}, HTTPStatus.OK
        # return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
# TODO: Описать провайдеров в extensions (гугл, яндекс, мейл).
# TODO: Проработать пайплайн авторизации:
#   1. получить токен и юзеринфо
#   2. проверить наличие провайдера в БД:
#      2.1 Если провайдер есть в БД, то получить юзера. Отдать токены
#      2.2 Если провайдера нет в БД, получить данные пользователя из токена.
#          Создать пользователя (поставить флаг, что зареган через сторонний сервис.). При смене пароля мы не запрашиваем у пользователя old_password.
#          Добавить провайдера в БД. Авторизовать пользователя (отдать токены).
