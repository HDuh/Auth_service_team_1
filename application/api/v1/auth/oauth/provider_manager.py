from dataclasses import dataclass
from typing import Any

from flask import url_for, request
from urllib.parse import urlparse
from http import HTTPStatus


@dataclass
class ProviderManager:
    """Менеджер провайдеров"""
    provider: Any

    def authorize(self):
        """Метод авторизации. Если запрос идет со swagger'а, то возвращается информация о редиректе"""
        redirect_uri = self.__get_callback_url()
        if 'swagger' in urlparse(request.referrer).path:
            return {'auth_provider': self.provider.name, 'redirect_uri': redirect_uri}, HTTPStatus.FOUND
        return self.provider.service.authorize_redirect(redirect_uri)

    def __get_callback_url(self) -> str:
        return url_for('auth.socialcallback', provider_name=self.provider.name, _external=True)
