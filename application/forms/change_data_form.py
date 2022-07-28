from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo

__all__ = (
    'ChangeDataForm',
)


class ChangeDataForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    old_password = PasswordField('Old_password', validators=[DataRequired()])
    new_password = PasswordField('New_password')
    new_password2 = PasswordField('Repeat_new_password', validators=[EqualTo('new_password'), ])
