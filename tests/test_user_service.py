from tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    def test_registration(self):
        self.user_service.register("test", "test")
        db_user = self.user_service.get_user("test")
        self.assertTrue(self.password_service.check_password("test", db_user.password))

    def test_login(self):
        self.authentication_service.register("test", "test")
        key = self.authentication_service.login("test", "test")
        self.session_service.get_session(key)

    def test_double_login_with_same_session(self):
        self.authentication_service.register("test", "test")
        first_key = self.authentication_service.login("test", "test")
        second_key = self.authentication_service.login("test", "test")
        self.assertEqual(first_key, second_key)
