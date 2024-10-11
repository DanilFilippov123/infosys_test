from db.models.user_dto import UserDTO
from db.orm.user_orm import UserModel
from db.session import Session


class UserRepository:

    def save(self, user: UserDTO) -> UserDTO:
        user_orm = UserModel(login=user.login,
                             password=user.password)
        with Session.begin() as session:
            session.add(user_orm)
            session.commit()

    def load(self, login):
        pass
