from flask import Blueprint
from flask_restful import Api

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

from . import routes
