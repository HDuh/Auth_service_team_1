import json
from http import HTTPStatus

import requests

from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_MAIL, TEST_SIGN_UP_DATA


class TestSignup(TestBase):
    def test_signup_user(self):
        auth = AuthActions()
        url = f"{auth.base_url}/signup"
        payload = json.dumps(TEST_SIGN_UP_DATA)

        response = requests.request("POST", url, headers=auth.headers, data=payload)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f'User {TEST_MAIL} successfully registered', response.json().get('message'))

    def test_signup_already_exist(self) -> None:
        auth = AuthActions()
        auth.signup()
        url = f"{auth.base_url}/signup"
        payload = json.dumps(TEST_SIGN_UP_DATA)

        response = requests.request("POST", url, headers=auth.headers, data=payload)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f'User {TEST_MAIL} already exist', response.json().get('message'))

    def test_signup_empty_data(self) -> None:
        auth = AuthActions()
        url = f"{auth.base_url}/signup"

        response = requests.request("POST", url, headers=auth.headers, data={})

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_signup_incorrect_mail(self) -> None:
        auth = AuthActions()
        url = f"{auth.base_url}/signup"
        payload = json.dumps({"email": "te.com",
                              "password": "incorrect",
                              "password2": "incorrect"})

        response = requests.request("POST", url, headers=auth.headers, data=payload)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual("email - 'Not a valid email address.'", response.json().get('message'))
