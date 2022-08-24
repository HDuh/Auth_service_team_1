import json
import unittest
from http import HTTPStatus

import requests

from application.app import db
from application.models import User, Role
from application.services.permissions import init_permissions, init_default_roles
from tests.functional.constants import TEST_LOGIN_DATA, TEST_SIGN_UP_DATA, TEST_ROLE_NAME
from tests.functional.utils import clear_tables
from .test_config import Config


class TestBase(unittest.TestCase):
    def setUp(self):
        db.create_all()
        init_permissions(db, Config)
        init_default_roles(db, Config)

    def tearDown(self):
        db.session.remove()
        clear_tables(db)


class AuthActions(object):
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.base_url = f"http://{Config.FLASK_HOST}:{Config.FLASK_PORT}"

    def signup(self, data=TEST_SIGN_UP_DATA):
        url = f"{self.base_url}/signup"
        payload = json.dumps(data)

        response = requests.request("POST", url, headers=self.headers, data=payload)
        assert response.status_code == HTTPStatus.OK

    def login(self, data=TEST_LOGIN_DATA):
        self.signup()
        url = f"{self.base_url}/login"
        payload = json.dumps(data)
        response = requests.request("POST", url, headers=self.headers, data=payload)
        assert response.status_code == HTTPStatus.OK

        self.access_token = response.json().get('access_token')
        self.refresh_token = response.json().get('refresh_token')

    def admin_login(self, data=TEST_LOGIN_DATA):
        self.login()
        user = User.query.filter_by(email=TEST_LOGIN_DATA.get('email')).first()
        role = Role.query.filter_by(role_name='admin').first()
        user.role.append(role)
        db.session.commit()

        url = f"{self.base_url}/login"

        payload = json.dumps(data)
        response = requests.request("POST", url, headers=self.headers, data=payload)

        assert response.status_code == HTTPStatus.OK

        self.access_token = response.json().get('access_token')
        self.refresh_token = response.json().get('refresh_token')

    def logout(self):
        ...


class RoleActions(object):
    def __init__(self):
        self.auth = AuthActions()
        self.auth.admin_login()
        self.url = f"{self.auth.base_url}/role"
        self.auth.headers.update({'Authorization': f'Bearer {self.auth.access_token}'})
        self.headers = self.auth.headers

    def create_role(self, role_name=TEST_ROLE_NAME):
        payload = json.dumps({'role_name': role_name,
                              'permissions': Config.BASE_PERMISSIONS[:2]})
        response = requests.request("POST", self.url, headers=self.headers, data=payload)

        return response

    def update_role(self, new_role_name, role_name=TEST_ROLE_NAME):
        payload = json.dumps({'role_name': role_name,
                              'new_role_name': new_role_name,
                              'permissions': Config.BASE_PERMISSIONS[2:]})
        response = requests.request("PATCH", self.url, headers=self.headers, data=payload)

        return response

    def delete_role(self, role_name):
        payload = json.dumps({'role_name': role_name})
        response = requests.request("DELETE", self.url, headers=self.headers, data=payload)

        return response
