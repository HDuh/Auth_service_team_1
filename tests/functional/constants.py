from dataclasses import dataclass, asdict

TEST_MAIL = 'tester@test.com'
TEST_ROLE_NAME = 'test_role'


@dataclass
class TestSignUpUser:
    email: str = TEST_MAIL
    password: str = '1234567'
    password2: str = '1234567'


@dataclass
class TestLoginUser:
    email: str = TEST_MAIL
    password: str = '1234567'


@dataclass
class TestChangeDataUser:
    email: str = TEST_MAIL
    old_password: str = TestLoginUser.password
    new_password: str = '12345678'
    new_password2: str = '12345678'


TEST_LOGIN_DATA = asdict(TestLoginUser())
TEST_SIGN_UP_DATA = asdict(TestSignUpUser())
