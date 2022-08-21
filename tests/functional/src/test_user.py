import uuid
from http import HTTPStatus

import requests
from flask.testing import FlaskClient

from application.extensions import db
from application.models import User, Role
from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_MAIL


class TestUser(TestBase):
    def test_get_profile_info(self):
        auth = AuthActions()
        auth.admin_login()
        user = User.query.filter_by(email=TEST_MAIL).first()
        user_id = user.get_id()
        url = f"{auth.base_url}/user/{user_id}"
        headers = {'Authorization': f'Bearer {auth.access_token}'}

        response = requests.request("GET", url, headers=headers)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(user_id, response.json().get('user_id'))

    def test_get_profile_info_not_exist(self):
        auth = AuthActions()
        auth.admin_login()
        test_id = uuid.uuid4()
        url = f"{auth.base_url}/user/{test_id}"
        headers = {'Authorization': f'Bearer {auth.access_token}'}

        response = requests.request("GET", url, headers=headers)

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(f'User id {test_id} not found', response.json().get('message'))

    def test_get_auth_history(self):
        auth = AuthActions()
        auth.admin_login()
        user = User.query.filter_by(email=TEST_MAIL).first()
        user_id = user.get_id()
        url = f"{auth.base_url}/user/{user_id}/auth_history"
        headers = {'Authorization': f'Bearer {auth.access_token}'}

        response = requests.request("GET", url, headers=headers)

        signup_info = response.json()[0]
        login_info = response.json()[1]
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(3, len(response.json()))
        self.assertEqual(user_id, signup_info.get('user_id'))
        self.assertEqual('signup', signup_info.get('action'))
        self.assertEqual('login', login_info.get('action'))

    def test_get_auth_history_not_exist(self):
        auth = AuthActions()
        auth.admin_login()
        test_id = uuid.uuid4()
        url = f"{auth.base_url}/user/{test_id}/auth_history"
        headers = {'Authorization': f'Bearer {auth.access_token}'}

        response = requests.request("GET", url, headers=headers)

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(f'User id {test_id} not found', response.json().get('message'))