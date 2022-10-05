from http import HTTPStatus

from flask_apispec import doc, MethodResource, marshal_with
from flask_restful import Resource, abort

from core.providers_map import ProvidersMap
from schemas.responses_schemas import ResponseSchema, SwaggerSocialResponse

__all__ = (
    'SocialAuthorize',
    'SocialCallback',
)


class SocialAuthorize(Resource, MethodResource):
    """ Обращение к провайдеру """

    @doc(
        tags=['SocialAuth'],
        description='Authorize with external services',
        summary='User authorize',
    )
    @marshal_with(SwaggerSocialResponse, code=302, description='Server response', apply=False)
    @marshal_with(ResponseSchema, code=400, description='Bad server response', apply=False)
    def get(self, provider_name: str):
        if provider_name not in ProvidersMap.__annotations__:
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'Provider {provider_name} not supported')
        provider = ProvidersMap.__annotations__[provider_name]
        return provider.manager.authorize()


class SocialCallback(Resource):
    """ Обработка обратного вызова от провайдера """

    @staticmethod
    def get(provider_name: str):
        provider = ProvidersMap.__annotations__[provider_name]
        return provider.callback()
