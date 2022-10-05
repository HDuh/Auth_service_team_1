from marshmallow import Schema, validate, ValidationError, validates_schema
from marshmallow.fields import Str, Email

__all__ = (
    'SignUpSchema',
    'LoginSchema',
    'ChangeDataSchema',
)


class SignUpSchema(Schema):
    """Форма регистрации"""

    email = Email(required=True, validate=validate.Length(min=5, max=256))
    password = Str(required=True, validate=validate.Length(min=6, max=256))
    password2 = Str(required=True, validate=validate.Length(min=6, max=256))

    @validates_schema
    def validate_eq_passwords(self, schema, **kwargs):
        if schema['password'] != schema['password2']:
            raise ValidationError('Passwords password and password2 should be equal')


class LoginSchema(Schema):
    """Форма аутентификации"""

    email = Email(required=True, validate=validate.Length(min=5, max=256))
    password = Str(required=True, validate=validate.Length(min=6, max=256))


class ChangeDataSchema(Schema):
    """Форма изменения данных пользователя"""

    email = Email(required=True, validate=validate.Length(min=5, max=256))
    old_password = Str(required=True, validate=validate.Length(min=6, max=256))
    new_password = Str(validate=validate.Length(min=6, max=256))
    new_password2 = Str(validate=validate.Length(min=6, max=256))

    @validates_schema
    def compare_passwords(self, schema, **kwargs):
        if schema['new_password'] != schema['new_password2']:
            raise ValidationError('Passwords password and password2 should be equal')

    @validates_schema
    def validate_eq_passwords(self, schema, **kwargs):
        if schema['old_password'] == schema['new_password']:
            raise ValidationError('Passwords old and new should be different')
