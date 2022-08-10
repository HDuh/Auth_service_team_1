from functools import wraps
from http import HTTPStatus

from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restful import abort


def validate_form(form=None):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            f = form()
            if not (error := f.validate(request.json)):
                return func(*args, **kwargs)
            errors: list = []
            incorrect_params: list = [i for i in error]
            for param_i in incorrect_params:
                errors.append(f"{param_i} - '{error.get(param_i)[0]}'")

            error_message = ', '.join(errors)

            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=error_message)

        return inner

    return func_wrapper


def role_access(*access_roles):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user_roles = get_jwt_identity()['roles']
            if not any(role in access_roles for role in user_roles):
                abort(http_status_code=HTTPStatus.FORBIDDEN, message='Access denied')

            return func(*args, **kwargs)

        return inner

    return func_wrapper
