from pydantic import constr, validator, EmailStr

from app.models.api.base import BaseApiModel


class BaseUser(BaseApiModel):
    username: constr(min_length=6, max_length=128)
    password: constr(min_length=6)
    fullname: constr(min_length=6, max_length=255)
    mail: EmailStr


class User(BaseUser):
    confirm_password: constr(min_length=6)

    @validator('confirm_password')
    def passwords_match(cls, password, values):
        if 'password' in values and password != values['password']:
            raise ValueError('passwords do not match')
        return password
