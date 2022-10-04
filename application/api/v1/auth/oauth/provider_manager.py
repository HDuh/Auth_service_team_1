from dataclasses import dataclass
from typing import Any

from flask import url_for


@dataclass
class ProviderManager:
    """Менеджер провайдеров"""
    provider: Any

    def authorize(self) -> None:
        redirect_uri = self.__get_callback_url()
        return self.provider.service.authorize_redirect(redirect_uri)

    def __get_callback_url(self) -> str:
        return url_for('auth.socialcallback', provider_name=self.provider.name, _external=True)
