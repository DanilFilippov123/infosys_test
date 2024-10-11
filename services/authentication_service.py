from errors.authentication_erros import InvalidPassword, AuthenticationError
from errors.user_errors import UserError
from services.challenge_service import ChallengeService
from services.dh_service import DHService
from services.password_service import PasswordService
from services.session_service import SessionService
from services.user_service import UserService


class AuthenticationService:
    def __init__(self,
                 prime: int,
                 generator: int,
                 dh_service: DHService,
                 session_service: SessionService,
                 user_service: UserService,
                 password_service: PasswordService,
                 challenge_service: ChallengeService) -> None:
        self.challenge_service = challenge_service
        self.password_service = password_service
        self.session_service = session_service
        self.user_service = user_service
        self.prime = prime
        self.generator = generator
        self.dh = dh_service

    def register(self,
                 login: str,
                 password: str) -> str:
        try:
            self.user_service.register(login, password)
        except UserError as e:
            raise AuthenticationError(e)
        return "ok"

    def login(self, login: str, password: str) -> str:
        user = self.user_service.get_user(login)
        if self.password_service.check_password(password, user.password):
            session = self.session_service.get_or_create(user)
            return session.key.hex
        else:
            raise InvalidPassword

    def logout(self, session_key: str) -> str:
        self.session_service.delete(session_key)
        return "ok"

    def get_public_keys(self) -> tuple[int, int]:
        return self.dh.get_public_keys()

    def get_partial_key(self, session_key: str) -> int:
        session = self.session_service.get_session(session_key)
        server_private_key = self.dh.generate_private_key()
        session.server_private_key = server_private_key
        self.session_service.save_session(session)

        return self.dh.generate_partial_key(server_private_key)

    def get_full_key(self, session_key: str, partial_key: int) -> str:
        session = self.session_service.get_session(session_key)
        if session.server_private_key is None:
            raise AuthenticationError("First get partial key")
        session.secret = self.dh.generate_full_key(partial_key, session.server_private_key)
        session.server_private_key = None
        self.session_service.save_session(session)
        return "ok"

    def get_challenge(self, session_key: str) -> str:
        session = self.session_service.get_session(session_key)
        challenge = self.challenge_service.get_challenge()
        session.challenge = challenge
        self.session_service.save_session(session)
        return challenge
