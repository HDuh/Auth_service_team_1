import json
from http import HTTPStatus

import requests

from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_LOGIN_DATA


class TestLogin(TestBase):
    def test_login_user(self):
        auth = AuthActions()
        auth.signup()
        url = f"{auth.base_url}/login"
        payload = json.dumps(TEST_LOGIN_DATA)

        response = requests.request("POST", url, headers=auth.headers, data=payload)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn('access_token', response.json())
        self.assertIn('refresh_token', response.json())

    def test_incorrect_login_user(self):
        auth = AuthActions()
        auth.signup()
        url = f"{auth.base_url}/login"
        payload = json.dumps({"email": "tester@test.com", "password": "incorrect"})

        response = requests.request("POST", url, headers=auth.headers, data=payload)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Incorrect login or password', response.json().get("message"))
