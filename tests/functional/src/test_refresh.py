import unittest
from http import HTTPStatus

from application.core.config import Config
from application.main import app, db, init_api
from tests.functional.constants import TEST_USER_DATA, TEST_LOGIN_DATA
from tests.functional.utils import clear_tables


class TestRefresh(unittest.TestCase):
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

    def setUp(self) -> None:
        # registration user
        response = app.test_client().post("/signup", data=TEST_USER_DATA)
        assert response.status_code == HTTPStatus.OK

        # login user
        response = app.test_client().post("/login", data=TEST_LOGIN_DATA)
        assert response.status_code == HTTPStatus.OK

        self.access_token = response.json.get("access_token")
        self.refresh_token = response.json.get("refresh_token")

    def tearDown(self) -> None:
        db.session.remove()
        clear_tables(db)

    def test_refresh(self) -> None:
        headers = {"Authorization": f"Bearer {self.refresh_token}"}

        response = self.app.post("/refresh_token", data=TEST_LOGIN_DATA, headers=headers)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("access_token", response.json)
        self.assertIn("refresh_token", response.json)

    def test_incorrect_token(self) -> None:
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = self.app.post("/refresh_token", data=TEST_LOGIN_DATA, headers=headers)

        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual("Only refresh tokens are allowed", response.json.get("msg"))

    def test_incorrect_header(self) -> None:
        response = self.app.post("/refresh_token", data=TEST_LOGIN_DATA, headers={"Authorization": "Bearer test"})
        self.assertEqual(HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual("Not enough segments", response.json.get("msg"))

    def test_empty_header(self) -> None:
        response = self.app.post("/refresh_token", data=TEST_LOGIN_DATA, headers='')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertEqual("Missing Authorization Header", response.json.get("msg"))


if __name__ == '__main__':
    unittest.main()
