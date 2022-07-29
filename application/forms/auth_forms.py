from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import Email, DataRequired, EqualTo, InputRequired, Optional, optional, ValidationError

__all__ = (
    'SignUpForm',
    'LoginForm',
    'ChangeDataForm',
)


class SignUpForm(FlaskForm):
    """Форма регистрации"""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    """Форма аутентификации"""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class ChangeDataForm(FlaskForm):
    """Форма изменения данных пользователя"""

    email = EmailField('Email', validators=[optional(), Email()])
    old_password = PasswordField('Old_password', validators=[DataRequired()])
    new_password = PasswordField('New_password', validators=[])
    new_password2 = PasswordField('Repeat_new_password', validators=[EqualTo('new_password'), ])

    def validate_passwords(self, new_password):
        if new_password == self.old_password:
            raise ValidationError('Passwords old and new should be different')
