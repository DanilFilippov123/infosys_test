from db.models.data_dto import DataDTO
from db.repositories.data_repository import DataRepository
from errors.authentication_erros import AuthenticationError
from services.session_service import SessionService
from services.user_signatur_service import UserSignatureService


class DataService:

    def __init__(self,
                 session_service: SessionService,
                 data_repository: DataRepository,
                 user_signature_service: UserSignatureService) -> None:
        self.user_signature_service = user_signature_service
        self.data_repository = data_repository
        self.session_service = session_service

    def get_data(self,
                 session_key: str,
                 key: str,
                 signature: str) -> DataDTO:
        session = self.session_service.get_session(session_key)
        if self.user_signature_service.validate_signature(signature,
                                                          session.challenge,
                                                          session.secret):
            return self.data_repository.load(key)

        raise AuthenticationError("Invalid signature")

    def insert(self,
               session_key: str,
               key: str,
               value: str,
               signature: str):
        session = self.session_service.get_session(session_key)
        if self.user_signature_service.validate_signature(signature,
                                                          session.challenge,
                                                          session.secret):
            self.data_repository.save(DataDTO(key=key,
                                              data=value))
            return "ok"
        raise AuthenticationError("Invalid signature")
