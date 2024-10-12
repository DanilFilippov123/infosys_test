import secrets
import unittest.mock
import xmlrpc.client
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db.session

# Create an in-memory SQLite database
sqlight_engine = create_engine("sqlite:///:memory:", echo=True)
setattr(db.session, 'Session', sessionmaker(sqlight_engine))

import db.orm.base_orm
import db.orm.session_orm
import db.orm.user_orm
import db.orm.data_orm

import config
import server
from db.repositories.data_repository import DataRepository
from db.repositories.session_repository import SessionRepository
from db.repositories.user_repository import UserRepository
from services.authentication_service import AuthenticationService
from services.challenge_service import ChallengeService
from services.data_service import DataService
from services.dh_service import DHService
from services.password_service import PasswordService
from services.session_service import SessionService
from services.user_service import UserService
from services.user_signatur_service import UserSignatureService


class BaseServicesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_model = db.orm.base_orm.Base
        base_model.metadata.create_all(sqlight_engine)

        cls.password_service = PasswordService()
        cls.session_repo = SessionRepository()
        cls.session_service = SessionService(cls.session_repo)
        cls.user_repo = UserRepository()
        cls.user_service = UserService(cls.user_repo,
                                       cls.password_service)
        cls.challenge_service = ChallengeService()
        cls.authentication_service = AuthenticationService(
            23,
            2,
            DHService(23, 2),
            cls.session_service,
            cls.user_service,
            cls.password_service,
            cls.challenge_service
        )
        cls.data_repo = DataRepository()
        cls.user_signature_service = UserSignatureService()
        cls.data_service = DataService(cls.session_service,
                                       cls.data_repo,
                                       cls.user_signature_service)

    def get_secret(self, session_key):
        pk = secrets.randbits(16)

        prime, generator = self.authentication_service.get_public_keys()

        our_partial_key = pow(generator, pk, prime)

        server_partial_key = self.authentication_service.get_partial_key(session_key,
                                                                         our_partial_key)

        return pow(server_partial_key, pk, prime)


class BaseServerTestCase(unittest.TestCase):
    class ServerThread(Thread):
        def __init__(self):
            super().__init__()
            self.server = server.server

        def run(self):
            base_model = db.orm.base_orm.Base
            base_model.metadata.create_all(sqlight_engine)
            self.server.serve_forever()

        def kill(self):
            self.server.shutdown()

    server_thread: ServerThread = None

    client = xmlrpc.client.ServerProxy(
        f"http://{config.address[0]}:{config.address[1]}/"
    )

    @classmethod
    def setUpClass(cls):
        cls.server_thread = cls.ServerThread()
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server_thread.kill()
        cls.server_thread.join()
