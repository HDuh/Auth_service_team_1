from dataclasses import dataclass, asdict

TEST_MAIL = 'tester@test.com'
TEST_ROLE_NAME = 'test_role'


@dataclass
class TestLoginUser:
    email: str = TEST_MAIL
    password: str = '123'
    password2: str = '123'


@dataclass
class TestChangeDataUser:
    email: str = TEST_MAIL
    old_password: str = TestLoginUser.password
    new_password: str = '1234'
    new_password2: str = '1234'


TEST_LOGIN_DATA = asdict(TestLoginUser())
TEST_USER_DATA = asdict(TestLoginUser())
