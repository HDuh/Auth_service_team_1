from http import HTTPStatus

from flask.testing import FlaskClient

from tests.functional.conftest import TestBase, AuthActions
from tests.functional.constants import TEST_USER_DATA


class TestChangeLoginPassword(TestBase):
    def test_change_login(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'email': 'new_tester@test.com',
                'old_password': TEST_USER_DATA.get('password')}

        response = client.post('/change_auth_data', data=data, headers=headers)
        print('')
        print(response.json)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Login change successfully', response.json.get('message'))

    def test_change_password(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        new_pass = 'new_pass'
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'old_password': TEST_USER_DATA.get('password'),
                'new_password': new_pass,
                'new_password2': new_pass}

        response = client.post('/change_auth_data', data=data, headers=headers)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Password change successfully', response.json.get('message'))

    def test_change_login_and_password(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        new_pass = 'new_pass'
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'email': 'new_tester@test.com',
                'old_password': TEST_USER_DATA.get('password'),
                'new_password': new_pass,
                'new_password2': new_pass}

        response = client.post('/change_auth_data', data=data, headers=headers)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            'Login and password change successfully', response.json.get('message')
        )

    def test_change_login_empty_data(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        headers = {'Authorization': f'Bearer {auth.access_token}'}

        response = client.post('/change_auth_data', data={}, headers=headers)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Incorrect params', response.json.get('message'))

    def test_change_login_already_exist(self, client: FlaskClient):
        # user registration
        auth = AuthActions(client)
        auth.login()
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'email': TEST_USER_DATA.get('email'),
                'old_password': TEST_USER_DATA.get('password')}

        response = client.post('/change_auth_data', data=data, headers=headers)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Login already exist', response.json.get('message'))

    def test_change_password_incorrect_old_password(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        new_pass = 'new_pass'
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'old_password': 'incorrect_pass',
                'new_password': new_pass,
                'new_password2': new_pass}

        response = client.post('/change_auth_data', data=data, headers=headers)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Incorrect old password', response.json.get('message'))

    def test_change_password_incorrect_password2(self, client: FlaskClient):
        auth = AuthActions(client)
        auth.login()
        new_pass = 'new_pass'
        headers = {'Authorization': f'Bearer {auth.access_token}'}
        data = {'old_password': TEST_USER_DATA.get('password'),
                'new_password': new_pass,
                'new_password2': 'incorrect pass'}

        response = client.post('/change_auth_data', data=data, headers=headers)

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Incorrect params', response.json.get('message'))
