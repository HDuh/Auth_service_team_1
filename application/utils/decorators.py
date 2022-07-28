from functools import wraps
from http import HTTPStatus

from flask_restful import abort


def validate_form(form=None):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            f = form()
            if f.validate_on_submit():
                return func(*args, **kwargs)
            abort(http_status_code=HTTPStatus.BAD_REQUEST, message='Incorrect params')

        return inner

    return func_wrapper
