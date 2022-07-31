from http import HTTPStatus

from flask.testing import FlaskClient

from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_LOGIN_DATA


class TestLogout(TestBase):
    def test_logout_user(self, client: FlaskClient) -> None:
        auth = AuthActions(client)
        auth.login()
        headers = {"Authorization": f"Bearer {auth.access_token}"}

        response = client.post("/logout", data=TEST_LOGIN_DATA, headers=headers)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("Successfully logged out", response.json.get("message"))

    def test_logout_user_incorrect_token(self, client: FlaskClient) -> None:
        auth = AuthActions(client)
        auth.login()
        headers = {"Authorization": f"Bearer {auth.refresh_token}"}

        response = client.post("/logout", data=TEST_LOGIN_DATA, headers=headers)

        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual("Only non-refresh tokens are allowed", response.json.get("msg"))

    def test_logout_user_incorrect_header(self, client: FlaskClient) -> None:
        response = client.post("/logout", data=TEST_LOGIN_DATA, headers={"Authorization": "Bearer test"})
        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual("Not enough segments", response.json.get("msg"))

    def test_logout_user_empty(self, client: FlaskClient) -> None:
        response = client.post("/logout", data=TEST_LOGIN_DATA, headers='')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertEqual("Missing Authorization Header", response.json.get("msg"))
