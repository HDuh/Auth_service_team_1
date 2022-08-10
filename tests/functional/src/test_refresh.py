import json
from http import HTTPStatus

import requests

from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_LOGIN_DATA


class TestRefresh(TestBase):
    def test_refresh(self):
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/refresh_token"
        headers = {'Authorization': f'Bearer {auth.refresh_token}'}
        payload = json.dumps(TEST_LOGIN_DATA)

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn('access_token', response.json())
        self.assertIn('refresh_token', response.json())

    def test_incorrect_token(self):
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/refresh_token"
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        payload = json.dumps(TEST_LOGIN_DATA)

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual('Only refresh tokens are allowed', response.json().get('msg'))

    def test_incorrect_header(self):
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/refresh_token"
        headers = {'Authorization': 'Bearer test'}
        payload = json.dumps(TEST_LOGIN_DATA)

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual('Not enough segments', response.json().get('msg'))

    def test_empty_header(self):
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/refresh_token"
        headers = ''
        payload = json.dumps(TEST_LOGIN_DATA)

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertEqual('Missing Authorization Header', response.json().get('msg'))
