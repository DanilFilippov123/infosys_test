from db.models.session_dto import SessionDTO
from db.orm.session_orm import SessionModel
from db.orm.user_orm import UserModel
from db.repositories.base import Repository
from db.repositories.user_repository import UserRepository
from db.session import Session


class SessionRepository(Repository[SessionModel, SessionDTO]):

    @staticmethod
    def mapper_to_dto(session_orm: SessionModel) -> SessionDTO:
        return SessionDTO(
            expired_at=session_orm.expired_at,
            key=session_orm.key,
            secret=session_orm.secret,
            server_private_key=session_orm.server_private_key,
            challenge=session_orm.challenge,
            user=None
        )

    def save(self, session_dto: SessionDTO) -> SessionDTO:
        session_model = SessionModel(
            key=session_dto.key,
            secret=session_dto.secret,
            server_private_key=session_dto.server_private_key,
            challenge=session_dto.challenge,
            expired_at=session_dto.expired_at,
            user=UserRepository.mapper_to_dto(session_dto.user)
        )
        with Session() as session:
            user = session.get_one(UserModel, UserModel.login == session_dto.user.login)
            session_model.user = user
            session.add(session_model)
            session.commit()

        return session_dto

    def load(self, key: str) -> SessionDTO:
        with Session() as session:
            session_orm = session.get_one(SessionModel, SessionModel.key == key)
        return self.mapper_to_dto(session_orm)

    def delete(self, key: str) -> None:
        with Session() as session:
            session.delete(session.get_one(SessionModel, SessionModel.key == key))
            session.commit()
