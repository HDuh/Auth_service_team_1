from http import HTTPStatus

from flask import url_for, request
from flask_apispec import doc, marshal_with
from flask_restful import Resource, abort

from application.core import PROJECT_CONFIG
from application.extensions import providers, db
from application.models import Provider, AuthHistory
from application.models.models_enums import ActionsEnum
from application.schemas.responses_schemas import ResponseSchema
from application.services import get_tokens
from application.services.auth import register_provider_user


class SocialProvider(Resource):
    @doc(
        tags=['Social auth'],
        description='Auth through external service',
        summary='User auth'
    )
    @marshal_with(ResponseSchema, code=302, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    def get(self, provider_name: str):
        if provider_name not in providers:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'{provider_name} not supported')

        redirect_uri = url_for(f'auth.{provider_name}providerauth', _external=True, provider_name=provider_name)
        return providers.get(provider_name).authorize_redirect(redirect_uri)


class GoogleProviderAuth(Resource):
    @doc(
        tags=['Google'],
        description='Auth through google',
        summary='User auth'
    )
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    def get(self):
        token = providers.get('google').authorize_access_token()
        user_info = token['userinfo']
        provider = Provider.query.filter_by(id=int(user_info['sub'])).first()
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
    @doc(
        tags=['Yandex'],
        description='Auth through yandex',
        summary='User auth'
    )
    @marshal_with(ResponseSchema, code=200, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    def get(self):
        user_info = providers.get('yandex').userinfo()
        provider = Provider.query.filter_by(id=int(user_info['id'])).first()
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
    @doc(
        tags=['Mail'],
        description='Auth through mail',
        summary='User auth'
    )
    def get(self):
        token = providers.get('mail').authorize_access_token()
        userinfo = providers.get('mail').userinfo()
