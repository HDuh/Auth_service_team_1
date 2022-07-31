from http import HTTPStatus

from flask.testing import FlaskClient

from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_LOGIN_DATA


class TestLogin(TestBase):
    def test_login_user(self, client: FlaskClient):
        # user registration
        auth = AuthActions(client)
        auth.signup()

        response = client.post("/login", data=TEST_LOGIN_DATA)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("access_token", response.json)
        self.assertIn("refresh_token", response.json)

    def test_incorrect_login_user(self, client: FlaskClient) -> None:
        response = client.post("/login", data={"email": "test", "password": 'test'})

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Incorrect params', response.json.get("message"))
