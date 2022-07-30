import unittest
from http import HTTPStatus

from application.core.config import Config
from application.main import app, db, init_api
from tests.functional.constants import TEST_USER_DATA, TEST_LOGIN_DATA
from tests.functional.utils import clear_tables


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config['TESTING'] = True

        # test DataBase
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.TEST_DATABASE_URI

        # init test client
        cls.app = app.test_client()
        # api routes
        init_api()
        # init DataBase
        db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        # db.drop_all()
        pass

    def setUp(self) -> None:
        # registration user
        response = app.test_client().post("/signup", data=TEST_USER_DATA)
        assert response.status_code == HTTPStatus.OK

    def tearDown(self) -> None:
        db.session.remove()
        clear_tables(db)

    def test_login_user(self) -> None:
        response = self.app.post("/login", data=TEST_LOGIN_DATA)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("access_token", response.json)
        self.assertIn("refresh_token", response.json)

    def test_incorrect_login_user(self) -> None:
        response = self.app.post("/login", data={"email": "test", "password": 'test'})

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Incorrect login or password', response.json.get("message"))


if __name__ == '__main__':
    unittest.main()
