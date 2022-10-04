from http import HTTPStatus

from flask_restful import Resource, abort

from core.providers_map import ProvidersMap

__all__ = (
    'SocialAuthorize',
    'SocialCallback',
)


class SocialAuthorize(Resource):
    """ Обращение к провайдеру """

    @staticmethod
    def get(provider_name: str):
        if provider_name not in ProvidersMap.__annotations__:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'{provider_name} not supported')
        provider = ProvidersMap.__annotations__[provider_name]
        return provider.manager.authorize()


class SocialCallback(Resource):
    """ Обработка обратного вызова от провайдера """

    @staticmethod
    def get(provider_name: str):
        provider = ProvidersMap.__annotations__[provider_name]
        return provider.callback()
