from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

__all__ = (
    'RoleForm',
    'UpdateRoleForm'
)


class RoleForm(FlaskForm):
    role_name = StringField('Role', validators=[DataRequired()])


class UpdateRoleForm(FlaskForm):
    role_name = StringField('Role', validators=[DataRequired()])
    new_role_name = StringField('NewRole', validators=[DataRequired()])

    def validate_role_names(self, new_role_name):
        if new_role_name.data == self.role_name.data:
            raise ValidationError('Role name should be different')

# TODO: сделать инициализацию пермишинов при старте
