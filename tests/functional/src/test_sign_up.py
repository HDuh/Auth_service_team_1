import unittest
from http import HTTPStatus

from application.main import app, db, init_api
from application.core.config import Config
from application.models import User, Profile, AuthHistory

from tests.functional.utils import clear_tables
from tests.functional.constants import TEST_MAIL, TEST_USER_DATA


class TestSignUp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config['TESTING'] = True

        # test DataBase
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.TEST_DATABASE_URI

        # init test client
        cls.app = app.test_client()
        # api routes
        # init_api()
        # init DataBase
        db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        # db.drop_all()
        pass

    def tearDown(self) -> None:
        db.session.remove()
        clear_tables(db)

    def test_signup_user(self) -> None:
        response = self.app.post("/signup", data=TEST_USER_DATA)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f"User {TEST_MAIL} successfully registered", response.json.get('message'))

    def test_signup_user_in_db(self) -> None:
        self.app.post("/signup", data=TEST_USER_DATA)

        user = User.query.filter_by(email=TEST_MAIL).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()
        auth_history = AuthHistory.query.filter_by(user_id=user.id).first()

        self.assertEqual(user.email, TEST_MAIL)
        self.assertNotEqual(user, None)
        self.assertNotEqual(user_profile, None)
        self.assertNotEqual(auth_history, None)

    def test_signup_already_exist(self) -> None:
        # registration user
        self.app.post("/signup", data=TEST_USER_DATA)

        # registration already existed user
        response = self.app.post("/signup", data=TEST_USER_DATA)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f"User {TEST_MAIL} already exist", response.json.get('message'))

    def test_signup_incorrect_data(self) -> None:
        response = self.app.post("/signup", data={})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual("Incorrect login or password", response.json.get('message'))


if __name__ == '__main__':
    unittest.main()
