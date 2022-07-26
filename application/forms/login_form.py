from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, DataRequired

__all__ = (
    'LoginForm',
)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
