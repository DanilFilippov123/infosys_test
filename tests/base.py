import unittest

from sqlalchemy import text

from db.repositories.session_repository import SessionRepository
from db.repositories.user_repository import UserRepository
from db.session import engine
from services.authentication_service import AuthenticationService
from services.challenge_service import ChallengeService
from services.dh_service import DHService
from services.password_service import PasswordService
from services.session_service import SessionService
from services.user_service import UserService


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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

    def tearDown(self):
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE \"user\" RESTART IDENTITY CASCADE;"))
            conn.execute(text("TRUNCATE TABLE \"session\" RESTART IDENTITY CASCADE;"))
            conn.commit()
