from flask import url_for,session,redirect
from flask_restful import Resource

from application.extensions import google
from application.models import Client, User


class Google(Resource):
    def get(self):
        redirect_uri = url_for('auth.googleauth', _external=True)
        return google.authorize_redirect(redirect_uri)

class GoogleAuth(Resource):
    def get(self):
        token = google.authorize_access_token()
        userinfo = token['userinfo']
        session['user'] = userinfo
        return redirect('/login')