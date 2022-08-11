import json
from http import HTTPStatus

import requests
from flask.testing import FlaskClient

from tests.functional.conftest import TestBase, AuthActions, RoleActions
from tests.functional.constants import TEST_ROLE_NAME


class TestRoles(TestBase):
    def test_create(self):
        auth = AuthActions()
        auth.admin_login()
        url = f"{auth.base_url}/role"
        headers = auth.headers
        headers.update({'Authorization': f'Bearer {auth.access_token}'})
        payload = json.dumps({'role_name': TEST_ROLE_NAME})

        response = requests.request("POST", url, headers=auth.headers, data=payload)

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} created', response.json().get('message'))

    def test_already_exist(self):
        role = RoleActions()
        role.create_role(TEST_ROLE_NAME)

        response = role.create_role()

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} already exist', response.json().get('message'))

    def test_update(self):
        role = RoleActions()
        role.create_role(TEST_ROLE_NAME)

        response = role.update_role(role_name=TEST_ROLE_NAME,
                                    new_role_name='new_update_role')

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Role updated', response.json().get('message'))

    def test_update_not_existed(self):
        role = RoleActions()

        response = role.update_role(role_name='incorrect_role',
                                    new_role_name=TEST_ROLE_NAME)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Role not found', response.json().get('message'))

    def test_update_already_exist(self):
        role_name = 'existed name'
        role = RoleActions()
        role.create_role(TEST_ROLE_NAME)
        role.create_role(role_name)

        response = role.update_role(role_name=TEST_ROLE_NAME,
                                    new_role_name=role_name)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Role already exist', response.json().get('message'))

    def test_delete(self):
        role = RoleActions()
        role.create_role(TEST_ROLE_NAME)

        response = role.delete_role(TEST_ROLE_NAME)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} deleted', response.json().get('message'))

    def test_delete_not_existed(self):
        role = RoleActions()

        response = role.delete_role(TEST_ROLE_NAME)

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(f'Role {TEST_ROLE_NAME} not found', response.json().get('message'))
