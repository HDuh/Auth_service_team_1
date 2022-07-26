from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, DataRequired, EqualTo

__all__ = (
    'SignUpForm',
)


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Repeat password', validators=[DataRequired(), EqualTo('password')])
