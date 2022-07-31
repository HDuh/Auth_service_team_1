from http import HTTPStatus

from flask.testing import FlaskClient

from tests.functional.conftest import TestBase, AuthActions, RoleActions
from tests.functional.constants import TEST_ROLE_NAME


class TestRoles(TestBase):
    def test_create(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'role_name': TEST_ROLE_NAME}

        response = client.post('/role', data=data, headers=headers)

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} created', response.json.get('message'))

    def test_already_exist(self, client: FlaskClient):
        role = RoleActions(client)
        role.create_role(TEST_ROLE_NAME)

        response = role.create_role()

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} already exist', response.json.get('message'))

    def test_empty_header(self, client: FlaskClient):
        data = {'role_name': TEST_ROLE_NAME}

        response = client.post('/role', data=data, headers={})

        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertEqual('Missing Authorization Header', response.json.get('msg'))

    def test_empty_data(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        client.post('/role', data={}, headers=headers)

        response = client.post('/role', data={}, headers=headers)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Incorrect params', response.json.get('message'))

    def test_update(self, client: FlaskClient):
        role = RoleActions(client)
        role.create_role(TEST_ROLE_NAME)

        response = role.update_role(role_name=TEST_ROLE_NAME,
                                    new_role_name='new_update_role')

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Role updated', response.json.get('message'))

    def test_update_not_existed(self, client: FlaskClient):
        role = RoleActions(client)

        response = role.update_role(role_name='incorrect_role',
                                    new_role_name=TEST_ROLE_NAME)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Role not found', response.json.get('message'))

    def test_update_already_exist(self, client: FlaskClient):
        role_name = 'existed name'
        role = RoleActions(client)
        role.create_role(TEST_ROLE_NAME)
        role.create_role(role_name)

        response = role.update_role(role_name=TEST_ROLE_NAME,
                                    new_role_name=role_name)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Role already exist', response.json.get('message'))

    def test_delete(self, client: FlaskClient):
        role = RoleActions(client)
        role.create_role(TEST_ROLE_NAME)

        response = role.delete_role(TEST_ROLE_NAME)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} deleted', response.json.get('message'))

    def test_delete_not_existed(self, client: FlaskClient):
        role = RoleActions(client)

        response = role.delete_role(TEST_ROLE_NAME)

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} not found', response.json.get('message'))
