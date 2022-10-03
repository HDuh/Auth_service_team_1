from http import HTTPStatus

from flask_restful import Resource, abort

from api.v1.auth.oauth.social_auth import OAuthProvider
from extensions import providers


class SocialAuthorize(Resource):
    """ Обращение к провайдеру """
    @staticmethod
    def get(provider_name: str):
        if provider_name not in providers:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'{provider_name} not supported')

        oauth = OAuthProvider.get_provider(provider_name)
        return oauth.authorize()


class SocialCallback(Resource):
    """ Обработка обратного вызова от провайдера """
    @staticmethod
    def get(provider_name: str):
        oauth = OAuthProvider.get_provider(provider_name)
        return oauth.callback()
