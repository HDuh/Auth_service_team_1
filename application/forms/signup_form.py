from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError

from application.models import User

__all__ = (
    'SignUpForm',
)


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Repeat password', validators=[DataRequired(), EqualTo('password')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'User {user.email} already exist.')
