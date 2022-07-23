from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, DataRequired, ValidationError

__all__ = (
    'LoginForm',
)

from application.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(f'User {email} not registered.')
