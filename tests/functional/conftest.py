from http import HTTPStatus

import flask_unittest
from flask.testing import FlaskClient

from application.core import Config
from application.main import app, db, init_api
from tests.functional.constants import TEST_LOGIN_DATA, TEST_USER_DATA
from tests.functional.utils import clear_tables


class TestBase(flask_unittest.ClientTestCase):
    # test db configs
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.TEST_DATABASE_URI

    # init test client
    app = app

    # api routes
    init_api()

    # init DataBase
    db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        # db.drop_all()
        pass

    def setUp(self, client: FlaskClient) -> None:
        ...

    def tearDown(self, client: FlaskClient) -> None:
        db.session.remove()
        clear_tables(db)


class AuthActions(object):
    def __init__(self, client: FlaskClient):
        self._client = client
        self.access_token = None
        self.refresh_token = None

    def signup(self, data=TEST_USER_DATA):
        self._client.post("/signup", data=data)
        return True

    def login(self, data=TEST_LOGIN_DATA):
        self.signup()
        response = self._client.post("/login", data=data)

        assert response.status_code == HTTPStatus.OK

        self.access_token = response.json.get("access_token")
        self.refresh_token = response.json.get("refresh_token")

    def logout(self):
        ...
