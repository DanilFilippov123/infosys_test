import logging
from xmlrpc.server import SimpleXMLRPCServer

import config
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

logging.basicConfig(level=config.LOG_LEVEL, format="%(filename)s-%(asctime)s-%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def return_error_on_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return f"error: {e}"

    return wrapper


class XMLRPCServer:
    def __init__(self,
                 session_expire_time: int = 1,
                 password_salt_length: int = 16,
                 password_hashing_method: str = "sha256",
                 signature_hashing_method: str = "sha256",
                 challenge_length: int = 32,
                 prime: int = 23,
                 generator: int = 2):
        self.user_repo = UserRepository()
        self.session_repo = SessionRepository()
        self.data_repo = DataRepository()

        self.password_service = PasswordService(password_salt_length,
                                                password_hashing_method)

        self.user_service = UserService(
            self.user_repo,
            self.password_service
        )

        self.session_service = SessionService(
            self.session_repo,
            session_expire_time
        )

        self.user_signature_service = UserSignatureService(signature_hashing_method)

        self.challenge_service = ChallengeService(challenge_length)

        self.data_service = DataService(self.session_service,
                                        self.data_repo,
                                        self.user_signature_service)

        self.dh_service = DHService(prime, generator)

        self.authentication_service = AuthenticationService(
            prime,
            generator,
            self.dh_service,
            self.session_service,
            self.user_service,
            self.password_service,
            self.challenge_service
        )

    @return_error_on_exception
    def register(self,
                 login: str,
                 password: str) -> str:
        logger.info("Registering user: %s", login)
        return self.authentication_service.register(
            login,
            password
        )

    @return_error_on_exception
    def login(self,
              login: str,
              password: str) -> str:
        logger.info("Logging in user: %s", login)
        return self.authentication_service.login(
            login,
            password
        )

    @return_error_on_exception
    def logout(self, session_key: str) -> str:
        logger.info("Logging out user: %s", session_key)
        return self.authentication_service.logout(session_key)

    @return_error_on_exception
    def get_public_keys(self) -> tuple[int, int]:
        logger.info("Getting public keys")
        return self.authentication_service.get_public_keys()

    @return_error_on_exception
    def get_partial_key(self, session_key: str, partial_key: int) -> int:
        logger.info("Getting partial key")
        return self.authentication_service.get_partial_key(session_key,
                                                           partial_key)

    @return_error_on_exception
    def get_challenge(self,
                      session_key: str) -> str:
        logger.info("Getting challenge")
        return self.authentication_service.get_challenge(
            session_key
        )

    @return_error_on_exception
    def get_data(self,
                 session_key: str,
                 key: str,
                 signature: str) -> str:
        logger.info("Getting data for key %s session: %s", key, session_key)
        return self.data_service.get_data(session_key, key, signature).data

    @return_error_on_exception
    def insert_data(self,
                    session_key: str,
                    key: str,
                    data: str,
                    signature: str) -> str:
        return self.data_service.insert(session_key,
                                        key,
                                        data,
                                        signature)


server = SimpleXMLRPCServer(
    config.address,
    encoding='ascii'
)

server.register_instance(XMLRPCServer(prime=config.prime,
                                      generator=config.generator))
server.register_introspection_functions()
