import json
import unittest
from http import HTTPStatus

import requests

from src.core import PROJECT_CONFIG
from src.extensions import db
from src.models import User, Role
from src.services.permissions import init_permissions, init_default_roles
from .constants import TEST_LOGIN_DATA, TEST_SIGN_UP_DATA, TEST_ROLE_NAME
from .utils import clear_tables


class TestBase(unittest.TestCase):
    def setUp(self):
        db.create_all()
        init_permissions(db, PROJECT_CONFIG)
        init_default_roles(db, PROJECT_CONFIG)

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
        self.base_url = f"http://{PROJECT_CONFIG.FLASK_HOST}:{PROJECT_CONFIG.FLASK_PORT}"

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
                              'permissions': PROJECT_CONFIG.BASE_PERMISSIONS[:2]})
        response = requests.request("POST", self.url, headers=self.headers, data=payload)

        return response

    def update_role(self, new_role_name, role_name=TEST_ROLE_NAME):
        payload = json.dumps({'role_name': role_name,
                              'new_role_name': new_role_name,
                              'permissions': PROJECT_CONFIG.BASE_PERMISSIONS[2:]})
        response = requests.request("PATCH", self.url, headers=self.headers, data=payload)

        return response

    def delete_role(self, role_name):
        payload = json.dumps({'role_name': role_name})
        response = requests.request("DELETE", self.url, headers=self.headers, data=payload)

        return response
