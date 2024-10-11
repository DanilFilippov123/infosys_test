import secrets

from tests.base import BaseTestCase


class TestAuthentication(BaseTestCase):

    def test_getting_password(self):
        self.authentication_service.register("test", "test")
        session_key = self.authentication_service.login("test", "test")

        pk = secrets.randbits(16)

        prime, generator = self.authentication_service.get_public_keys()

        our_partial_key = pow(generator, pk, prime)

        server_partial_key = self.authentication_service.get_partial_key(session_key)

        final_key = pow(server_partial_key, pk, prime)

        self.authentication_service.get_full_key(session_key, our_partial_key)

        session = self.session_service.get_session(session_key)

        self.assertEqual(session.secret, final_key)

