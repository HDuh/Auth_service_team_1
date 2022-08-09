from http import HTTPStatus

import requests

from tests.functional.conftest import TestBase, AuthActions


class TestLogout(TestBase):
    def test_logout_user(self):
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/logout"
        headers = {'Authorization': f'Bearer {auth.access_token}'}

        response = requests.request("POST", url, headers=headers)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Successfully logged out', response.json().get('message'))

    def test_logout_user_incorrect_token(self) -> None:
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/logout"
        headers = {'Authorization': f'Bearer {auth.refresh_token}'}

        response = requests.request("POST", url, headers=headers)

        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual('Only non-refresh tokens are allowed', response.json().get('msg'))

    def test_logout_user_incorrect_header(self) -> None:
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/logout"

        response = requests.request("POST", url, headers={'Authorization': 'Bearer test'})

        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual('Not enough segments', response.json().get('msg'))

    def test_logout_user_empty(self) -> None:
        auth = AuthActions()
        auth.login()
        url = f"{auth.base_url}/logout"

        response = requests.request("POST", url, headers='')

        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertEqual('Missing Authorization Header', response.json().get('msg'))
