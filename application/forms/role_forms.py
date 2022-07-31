from flask_wtf import FlaskForm
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired

__all__ = (
    'RoleForm',
    'UpdateRoleForm'
)


class RoleForm(FlaskForm):
    role_name = StringField('Role', validators=[DataRequired()])
    permissions = FieldList(StringField('Permission'), validators=[DataRequired()])


class UpdateRoleForm(FlaskForm):
    role_name = StringField('Role', validators=[DataRequired()])
    new_role_name = StringField('NewRole', validators=[DataRequired()])
    permissions = FieldList(StringField('Permissions'), validators=[DataRequired()])
