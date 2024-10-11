import datetime

from db.models.session_dto import SessionDTO
from db.models.user_dto import UserDTO
from db.repositories.session_repository import SessionRepository
from errors import session_errors


class SessionService:

    def __init__(self,
                 session_repository: SessionRepository,
                 session_expire_time_hours=1):
        self.session_repository = session_repository
        self._session_expire_time_hours = session_expire_time_hours

    def get_session(self, key: str) -> SessionDTO:
        session = self.session_repository.load(key)
        if session.expired_at > datetime.datetime.now():
            self.session_repository.delete(key)
            raise session_errors.SessionExpired(f"Session {key} expired")
        return session

    def save_session(self, session: SessionDTO) -> SessionDTO:
        return self.session_repository.save(session)

    def create_session(self,
                       user: UserDTO) -> SessionDTO:
        expired_at = datetime.datetime.now() + datetime.timedelta(hours=self._session_expire_time_hours)
        session = SessionDTO(
            user=user,
            expired_at=expired_at
        )

        return self.session_repository.save(session)

    def get_or_create(self, user: UserDTO) -> SessionDTO:
        try:
            return self.get_session(user.session.key)
        except session_errors.SessionError:
            return self.create_session(user)

    def delete(self, session_key: str) -> None:
        self.session_repository.delete(session_key)
