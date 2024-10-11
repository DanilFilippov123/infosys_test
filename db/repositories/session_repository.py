from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from db.models.session_dto import SessionDTO
from db.orm.session_orm import SessionModel
from db.orm.user_orm import UserModel
from db.repositories.base import Repository
from db.repositories.user_repository import UserRepository
from db.session import Session
from errors.session_errors import NoSessionError, SessionError


class SessionRepository(Repository[SessionModel, SessionDTO]):

    @staticmethod
    def mapper_to_dto(session_orm: SessionModel) -> SessionDTO:
        return SessionDTO(
            expired_at=session_orm.expired_at,
            key=session_orm.key,
            secret=session_orm.secret,
            server_private_key=session_orm.server_private_key,
            challenge=session_orm.challenge,
            user=UserRepository.mapper_to_dto(session_orm.user)
        )

    def save(self, session_dto: SessionDTO) -> SessionDTO:
        session_model = SessionModel(
            key=session_dto.key,
            secret=session_dto.secret,
            server_private_key=session_dto.server_private_key,
            challenge=session_dto.challenge,
            expired_at=session_dto.expired_at
        )
        with Session() as session:
            try:
                user_orm = session.query(UserModel).where(UserModel.login == session_dto.user.login).one()
            except NoResultFound:
                raise SessionError("User not found")
            prev_session = session.execute(select(SessionModel)
                                           .where(SessionModel.key == session_model.key)).scalar_one_or_none()
            if prev_session is None:
                session_model.user = user_orm
                session.add(session_model)
            else:
                session_model = session.merge(session_model)
            session.commit()
            result = self.mapper_to_dto(session_model)

        return result

    def load(self, key: str) -> SessionDTO:
        try:
            with Session() as session:
                session_orm = session.get_one(SessionModel, key)
                result = self.mapper_to_dto(session_orm)
        except NoResultFound:
            raise NoSessionError("No session found")
        return result

    def delete(self, key: str) -> None:
        with Session() as session:
            session.delete(session.get_one(SessionModel, key))
            session.commit()
