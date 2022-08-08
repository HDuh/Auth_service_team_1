from marshmallow import Schema, validate, ValidationError, validates_schema
from marshmallow.fields import Str, List, Email

__all__ = (
    'RoleBase',
    'RoleForm',
    'UpdateRoleForm',
    'UserRoleForm'
)


class RoleBase(Schema):
    role_name = Str(required=True, validate=validate.Length(min=3, max=128))


class RoleForm(RoleBase):
    permissions = List(Str, required=True)


class UpdateRoleForm(RoleBase):
    new_role_name = Str(required=True, validate=validate.Length(min=3, max=128))
    permissions = List(Str, required=True)

    @validates_schema
    def validate_role_names(self, schema, **kwargs):
        if schema['new_role_name'] == schema['role_name']:
            raise ValidationError('Role name should be different')


class UserRoleForm(RoleBase):
    email = Email(required=True, validate=validate.Length(min=5, max=256))
