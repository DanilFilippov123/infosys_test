import uuid

from errors.session_errors import SessionError
from tests.base import BaseServicesTestCase


class TestAuthentication(BaseServicesTestCase):

    def test_getting_secret(self):
        self.authentication_service.register("test", "test")
        session_key = self.authentication_service.login("test", "test")

        key = self.get_secret(session_key)

        session = self.session_service.get_session(session_key)

        self.assertEqual(key, session.secret)

    def test_getting_challenge_without_session(self):
        with self.assertRaises(SessionError):
            self.authentication_service.get_challenge(uuid.uuid4().hex)

    def test_getting_challenge(self):
        self.authentication_service.register("test", "test")
        session_key = self.authentication_service.login("test", "test")
        challenge = self.authentication_service.get_challenge(session_key)

        session = self.session_service.get_session(session_key)

        self.assertEqual(challenge, session.challenge)
