from http import HTTPStatus

from flask import url_for, request
from flask_restful import Resource, abort

from core import PROJECT_CONFIG
from extensions import providers, db
from models import Provider, AuthHistory
from models.models_enums import ActionsEnum
from services import get_tokens
from services.auth import register_provider_user


class SocialProvider(Resource):
    """Не знаем как добавить это в swagger.
    Выполняется authorize_redirect, который возвращает страницу для выбора профиля."""

    def get(self, provider_name: str):
        if provider_name not in providers:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'{provider_name} not supported')

        redirect_uri = url_for(f'auth.{provider_name}providerauth', _external=True)
        return providers.get(provider_name).authorize_redirect(redirect_uri)


class GoogleProviderAuth(Resource):
    def get(self):
        token = providers.get('google').authorize_access_token()
        user_info = token['userinfo']
        provider = Provider.query.filter_by(id=user_info['sub']).first()
        if not provider:
            user = register_provider_user(
                email=user_info['email'],
                uid=user_info['sub'],
                provider='google',
                request=request,
                db=db,
                role=PROJECT_CONFIG.DEFAULT_ROLES
            )
        else:
            user = provider.user
            history_login = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
            db.session.add(history_login)

        db.session.commit()
        access_token, refresh_token = get_tokens(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class YandexProviderAuth(Resource):
    def get(self):
        yandex = providers.get('yandex')
        token = yandex.authorize_access_token()
        user_info = yandex.userinfo(params=token)
        provider = Provider.query.filter_by(id=user_info['id']).first()
        if not provider:
            user = register_provider_user(
                email=user_info['default_email'],
                uid=user_info['id'],
                provider='yandex',
                request=request,
                db=db,
                role=PROJECT_CONFIG.DEFAULT_ROLES
            )
        else:
            user = provider.user
            history_login = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
            db.session.add(history_login)

        db.session.commit()
        access_token, refresh_token = get_tokens(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class MailProviderAuth(Resource):
    def get(self):
        mail = providers.get('mail')
        token = mail.authorize_access_token()
        user_info = mail.userinfo(params={'access_token': token['access_token']})
        provider = Provider.query.filter_by(id=user_info['id']).first()
        if not provider:
            user = register_provider_user(
                email=user_info['email'],
                uid=user_info['id'],
                provider='mail',
                request=request,
                db=db,
                role=PROJECT_CONFIG.DEFAULT_ROLES
            )
        else:
            user = provider.user
            history_login = AuthHistory(user=user, user_agent=request.user_agent.string, action=ActionsEnum.LOGIN)
            db.session.add(history_login)

        db.session.commit()
        access_token, refresh_token = get_tokens(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
