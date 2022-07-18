from flask import Blueprint
from flask_restful import Api

bp_role = Blueprint('role', __name__)
api = Api(bp_role)

from . import routes
