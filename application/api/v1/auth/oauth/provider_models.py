from http import HTTPStatus

from core import GoogleClient, YandexClient, MailClient
from extensions import db, oauth
from services import register_provider_user, get_tokens, add_login_info, check_provider
from .oauth_mixins import ManagerMixIn
from .provider_meta import MetaProvider


class MailOAuth(ManagerMixIn, metaclass=MetaProvider):
    name = 'mail'

    @classmethod
    def callback(cls):
        token = cls.service.authorize_access_token()
        user_info = cls.service.userinfo(params={'access_token': token['access_token']})
        provider = check_provider(cls.name, user_info['id'])

        if not provider:
            user = register_provider_user(
                email=user_info['email'],
                uid=user_info['id'],
                provider=cls.name,
                database=db,
            )
        else:
            user = provider.user
            add_login_info(provider, db)

        access_token, refresh_token = get_tokens(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

    class Config:
        client = oauth.register(**MailClient().dict())


class YandexOAuth(ManagerMixIn, metaclass=MetaProvider):
    name = 'yandex'

    @classmethod
    def callback(cls):
        token = cls.service.authorize_access_token()
        user_info = cls.service.userinfo(params=token)
        provider = check_provider(cls.name, user_info['id'])

        if not provider:
            user = register_provider_user(
                email=user_info['default_email'],
                uid=user_info['id'],
                provider=cls.name,
                database=db,
            )
        else:
            user = provider.user
            add_login_info(provider, db)

        access_token, refresh_token = get_tokens(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

    class Config:
        client = oauth.register(**YandexClient().dict())


class GoogleOAuth(ManagerMixIn, metaclass=MetaProvider):
    name = 'google'

    @classmethod
    def callback(cls):
        token = cls.service.authorize_access_token()
        user_info = token['userinfo']
        provider = check_provider(cls.name, user_info['sub'])

        if not provider:
            user = register_provider_user(
                email=user_info['email'],
                uid=user_info['sub'],
                provider=cls.name,
                database=db,
            )
        else:
            user = provider.user
            add_login_info(provider, db)

        access_token, refresh_token = get_tokens(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

    class Config:
        client = oauth.register(**GoogleClient().dict())
