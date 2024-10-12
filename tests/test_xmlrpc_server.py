import hmac

from tests.base import BaseServerTestCase, sqlight_engine


class TestXLMRPCServer(BaseServerTestCase):

    def test_register(self):
        res = self.client.register("regist", "test")
        self.assertEqual(res, "ok")

    def test_authentication(self):
        register = self.client.register("test2", "test")
        self.assertEqual(register, "ok")

        session = self.client.login("test2", "test")
        self.assertIsNotNone(session)

    def test_inserting_and_getting_data(self):
        register = self.client.register("ins", "test")
        self.assertEqual(register, "ok")

        session = self.client.login("ins", "test")
        self.assertIsNotNone(session)

        challenge = self.client.get_challenge(session)
        self.assertIsNotNone(challenge)

        prime, generator = self.client.get_public_keys()
        self.assertIsNotNone(prime)

        pk = 17
        partial_key = pow(generator, pk, prime)

        servers_partial_key = self.client.get_partial_key(session, partial_key)

        secret = pow(servers_partial_key, pk, prime)

        signature = hmac.new(secret.to_bytes(),
                             challenge.encode(),
                             "sha256").hexdigest()
        msg = 'test'
        self.client.insert_data(session, "test_key", msg, signature)
        ret_data = self.client.get_data(session, "test_key", signature)
        self.assertEqual(msg, ret_data)
