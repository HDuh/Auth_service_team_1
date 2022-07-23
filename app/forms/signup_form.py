from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, Length

__all__ = (
    'SignUpForm',
)


class SignUpForm(FlaskForm):
    email = StringField('email', validators=(Email(message='incorrect'),))
    password = StringField('password', validators=(Length(min=1, message='password must not be empty'),))
    password2 = StringField('password2', validators=(Length(min=1, message='password must not be empty'),))
