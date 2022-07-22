from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, Length

__all__ = (
    'LoginForm',
)


class LoginForm(FlaskForm):
    email = StringField('email', validators=(Email(message='incorrect'),))
    password = StringField('password', validators=(Length(min=1, message='password must not be empty'),))
