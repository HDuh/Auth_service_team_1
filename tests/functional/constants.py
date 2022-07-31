TEST_MAIL = 'tester@test.com'
TEST_USER_DATA = {"email": TEST_MAIL, "password": "123", "password2": "123"}
TEST_LOGIN_DATA = {"email": TEST_MAIL, "password": TEST_USER_DATA.get("password")}

TEST_CHANGE_DATA = {"email": TEST_MAIL,
                    "old_password": TEST_USER_DATA.get("password"),
                    "new_password": "1234",
                    "new_password2": "1234"}
