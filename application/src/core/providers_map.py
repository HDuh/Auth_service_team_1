from dataclasses import dataclass

from api.v1.auth.oauth.provider_models import GoogleOAuth, MailOAuth, YandexOAuth

__all__ = (
    'ProvidersMap',
)


@dataclass
class ProvidersMap:
    mail: MailOAuth = MailOAuth
    google: GoogleOAuth = GoogleOAuth
    yandex: YandexOAuth = YandexOAuth
