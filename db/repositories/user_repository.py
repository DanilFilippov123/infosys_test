from db.models.user_dto import UserDTO
from db.orm.user_orm import UserModel
from db.repositories.base import Repository
from db.session import Session
from errors.user_errors import UserError


class UserRepository(Repository[UserModel, UserDTO]):

    @staticmethod
    def mapper_to_dto(user_orm: UserModel) -> UserDTO:
        return UserDTO(login=user_orm.login,
                       password=user_orm.password,
                       session_key=user_orm.session)

    def save(self, user: UserDTO) -> UserDTO:
        user_orm = UserModel(login=user.login,
                             password=user.password,
                             session=user.session_key if user.session_key else None)
        with Session.begin() as session:
            session.add(user_orm)
            session.commit()
        return user

    def load(self, login) -> UserDTO:
        try:
            with Session() as session:
                user_orm = session.get_one(UserModel, UserModel.login == login)
        # TODO: add exception
        except Exception:
            raise UserError("User not found")
        return self.mapper_to_dto(user_orm)

    def delete(self, key) -> None:
        with Session() as session:
            session.delete(session.get_one(UserModel, UserModel.session == key))
            session.commit()
