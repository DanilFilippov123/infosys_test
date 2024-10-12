import hmac

from sqlalchemy import text

from db.session import engine
from tests.base import BaseServicesTestCase


class TestDataService(BaseServicesTestCase):

    @classmethod
    def tearDownClass(cls):
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE \"data\" RESTART IDENTITY CASCADE;"))
            conn.commit()

    def test_setting_and_getting_data(self):
        self.authentication_service.register("test", "test")
        session_key = self.authentication_service.login("test", "test")
        challenge = self.authentication_service.get_challenge(session_key)

        secret_key = self.get_secret(session_key)

        signature = hmac.new(secret_key.to_bytes(),
                             challenge.encode(),
                             "sha256").hexdigest()
        msg = 'test'
        self.data_service.insert(session_key, "test_key", msg, signature)
        ret_data = self.data_service.get_data(session_key, "test_key", signature)
        self.assertEqual(msg, ret_data.data)
