from http import HTTPStatus

import flask_unittest
from flask.testing import FlaskClient

from .test_config import Config
from application.app import app, db, init_api
from tests.functional.constants import TEST_LOGIN_DATA, TEST_USER_DATA, TEST_ROLE_NAME
from tests.functional.utils import clear_tables

# TODO: заменить test DB на auth


class TestBase(flask_unittest.ClientTestCase):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.TEST_DATABASE_URI

    app = app
    init_api()
    db.create_all()

    @classmethod
    def setUpClass(cls) -> None:
        db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        db.drop_all()

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
        self._client.post('/signup', data=data)

    def login(self, data=TEST_LOGIN_DATA):
        self.signup()
        response = self._client.post('/login', data=data)

        assert response.status_code == HTTPStatus.OK

        self.access_token = response.json.get('access_token')
        self.refresh_token = response.json.get('refresh_token')

        return

    def logout(self):
        ...


class RoleActions(object):
    def __init__(self, client: FlaskClient):
        self._client = client

    def create_role(self, role_name=TEST_ROLE_NAME):
        # user registration
        auth = AuthActions(self._client)
        auth.login()
        # request params
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'role_name': role_name}

        return self._client.post('/role', data=data, headers=headers)

    def update_role(self, new_role_name, role_name=TEST_ROLE_NAME):
        # user registration
        auth = AuthActions(self._client)
        auth.login()

        # request params
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'role_name': role_name,
                'new_role_name': new_role_name}

        return self._client.patch('/role', data=data, headers=headers)

    def delete_role(self, role_name):
        # user registration
        auth = AuthActions(self._client)
        auth.login()

        # request params
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'role_name': role_name}

        return self._client.delete('/role', data=data, headers=headers)
