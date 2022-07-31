from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

__all__ = (
    'RoleForm',
    'UpdateRoleForm'
)


class RoleForm(FlaskForm):
    role_name = StringField('Role', validators=[DataRequired()])


class UpdateRoleForm(FlaskForm):
    role_name = StringField('Role', validators=[DataRequired()])
    new_role_name = StringField('NewRole', validators=[DataRequired()])

# TODO: сделать инициализацию пермишинов при старте
