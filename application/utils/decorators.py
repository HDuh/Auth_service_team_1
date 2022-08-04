from functools import wraps
from http import HTTPStatus
from flask import request

from flask_restful import abort


def validate_form(form=None):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            f = form()
            if not (error := f.validate(request.json)):
                return func(*args, **kwargs)
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message=f'Incorrect params {error}')

        return inner

    return func_wrapper
