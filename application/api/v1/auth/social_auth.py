from http import HTTPStatus

from flask import url_for, request
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from application.core import PROJECT_CONFIG
from application.extensions import google, db
from application.models import Provider, User, AuthHistory, Role
from application.models.models_enums import ActionsEnum
from application.services import get_tokens


class SocialProvider(Resource):
    def get(self, provider_name: str):
        redirect_uri = url_for('auth.socialproviderauth', _external=True, provider_name=provider_name)
        # TODO: после создания маппинга провайдеров, заменить в строке ниже google на provider_map.get(provider_name).
        #   Предусмотреть случаи, когда провайдера нет в разрешенных
        return google.authorize_redirect(redirect_uri)


class SocialProviderAuth(Resource):
    def get(self, provider_name: str):
        # TODO: заменить в строке ниже google на provider_map.get(provider_name)
        token = google.authorize_access_token()
        user_info = token['userinfo']
        provider = Provider.query.filter_by(id=int(user_info['sub'])).first()
        if not provider:
            user = User(
                email=user_info['email'],
                password=generate_password_hash(user_info['sub']),
                social_signup=True
            )
            new_provider = Provider(id=int(user_info['sub']), user=user, provider_name=provider_name)
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

    # TODO: Описать провайдеров в extensions (гугл, яндекс, мейл).
# TODO: Расширить таблицу юзера (добавить флаг регистрации через сторонний сервис)
# TODO: Создать таблицу Провайдеров (id (уникальный идентификатор пользователя из токена SUB), user_id (FK с таблицей юзеров), provider_name)
# TODO: Связать таблицу провайдеров с таблицей юзеров (one-to-many) (user это parent)
# TODO: Проработать пайплайн авторизации:
#   1. получить токен и юзеринфо
#   2. проверить наличие провайдера в БД:
#      2.1 Если провайдер есть в БД, то получить юзера. Отдать токены
#      2.2 Если провайдера нет в БД, получить данные пользователя из токена.
#          Создать пользователя (поставить флаг, что зареган через сторонний сервис.). При смене пароля мы не запрашиваем у пользователя old_password.
#          Добавить провайдера в БД. Авторизовать пользователя (отдать токены).
