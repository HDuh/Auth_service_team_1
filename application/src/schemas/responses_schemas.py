from marshmallow import Schema, fields


class ResponseSchema(Schema):
    message = fields.Str()


class AuthHistoryResponse(Schema):
    action = fields.Str()
    action_time = fields.DateTime()
    user_agent = fields.Str()
    user_id = fields.UUID()

    class Meta:
        dateformat = '%Y-%m-%dT%H:%M:%S+03:00'


class UserProfileResponse(Schema):
    profile_id = fields.UUID()
    user_id = fields.UUID()
    user_email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    country = fields.Str()


class SwaggerSocialResponse(Schema):
    provider_name = fields.Str()
    redirect_uri = fields.Str()
