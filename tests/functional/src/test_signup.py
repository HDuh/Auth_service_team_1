from http import HTTPStatus

from flask.testing import FlaskClient

from application.models import User, Profile, AuthHistory
from tests.functional.conftest import TestBase
from tests.functional.constants import TEST_MAIL, TEST_USER_DATA


class TestSignup(TestBase):
    def test_signup_user(self, client: FlaskClient):
        response = client.post("/signup", data=TEST_USER_DATA)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f"User {TEST_MAIL} successfully registered", response.json.get('message'))

    def test_signup_user_in_db(self, client: FlaskClient) -> None:
        client.post("/signup", data=TEST_USER_DATA)

        user = User.query.filter_by(email=TEST_MAIL).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()
        auth_history = AuthHistory.query.filter_by(user_id=user.id).first()

        self.assertEqual(user.email, TEST_MAIL)
        self.assertNotEqual(user, None)
        self.assertNotEqual(user_profile, None)
        self.assertNotEqual(auth_history, None)

    def test_signup_already_exist(self, client: FlaskClient) -> None:
        # registration user
        client.post("/signup", data=TEST_USER_DATA)

        # registration already existed user
        response = client.post("/signup", data=TEST_USER_DATA)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f"User {TEST_MAIL} already exist", response.json.get('message'))

    def test_signup_incorrect_data(self, client: FlaskClient) -> None:
        response = client.post("/signup", data={})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual("Incorrect login or password", response.json.get('message'))
