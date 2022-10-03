from http import HTTPStatus

from flask import url_for, request

from core import PROJECT_CONFIG
from extensions import providers, db
from models import Provider, AuthHistory
from models.models_enums import ActionsEnum
from services import register_provider_user, get_tokens


class OAuthProvider:
    """Базовый класс, определяет структуру реализации провайдера"""
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.service = providers.get(provider_name)

    def authorize(self):
        """ Обращение к провайдеру """
        redirect_uri = self.get_callback_url()
        return self.service.authorize_redirect(redirect_uri)

    def callback(self):
        """ Обработка обратного вызова с провайдера """
        pass

    def get_callback_url(self):
        """ Получение uri для конкретного провайдера """
        return url_for('auth.socialcallback', provider_name=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        """
        Используется для поиска правильного экземпляра OAuthProvider с именем поставщика.
        Этот метод использует интроспекцию для поиска всех подклассов OAuthProvider,
        а затем сохраняет экземпляр каждого в словаре.
        """
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class MailOAuth(OAuthProvider):
    def __init__(self):
        super(MailOAuth, self).__init__('mail')

    def callback(self):
        token = self.service.authorize_access_token()
        user_info = self.service.userinfo(params={'access_token': token['access_token']})
        provider = Provider.query\
            .filter_by(id=user_info['id'])\
            .filter_by(provider_name=self.provider_name)\
            .first()

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


class YandexOAuth(OAuthProvider):
    def __init__(self):
        super(YandexOAuth, self).__init__('yandex')

    def callback(self):
        token = self.service.authorize_access_token()
        user_info = self.service.userinfo(params=token)
        provider = Provider.query\
            .filter_by(id=user_info['id'])\
            .filter_by(provider_name=self.provider_name)\
            .first()
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


class GoogleOAuth(OAuthProvider):
    def __init__(self):
        super(GoogleOAuth, self).__init__('google')

    def callback(self):
        token = self.service.authorize_access_token()
        user_info = token['userinfo']
        provider = Provider.query\
            .filter_by(id=user_info['sub'])\
            .filter_by(provider_name=self.provider_name)\
            .first()
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
