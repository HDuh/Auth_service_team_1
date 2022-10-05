import json
from http import HTTPStatus

import requests

from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_LOGIN_DATA


class TestChangeLoginPassword(TestBase):
    def test_change_login_and_password(self):
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/change_auth_data"
        headers = auth.headers
        headers.update({'Authorization': f'Bearer {auth.access_token}'})

        new_pass = 'new_pass'
        payload = json.dumps({'old_password': TEST_LOGIN_DATA.get('password'),
                              'new_password': new_pass,
                              'new_password2': new_pass,
                              'email': 'sfsf@test.ru'})

        response = requests.request("POST", url, headers=auth.headers, data=payload)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            'Login and password change successfully', response.json().get('message')
        )

    def test_change_login_empty_data(self):
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/change_auth_data"
        headers = auth.headers
        headers.update({'Authorization': f'Bearer {auth.access_token}'})

        response = requests.request("POST", url, headers=auth.headers, data=json.dumps(''))

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
