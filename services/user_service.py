from db.models.user_dto import UserDTO
from db.repositories.user_repository import UserRepository
from services.password_service import PasswordService


class UserService:

    def __init__(self,
                 user_repository: UserRepository,
                 password_service: PasswordService) -> None:
        self.user_repository = user_repository
        self.password_service = password_service

    def create_user(self, user: UserDTO) -> UserDTO:
        return self.user_repository.save(user)

    def get_user(self, login: str) -> UserDTO:
        return self.user_repository.load(login)

    def register(self, login, password) -> UserDTO:
        user = UserDTO(login=login, password=self.password_service.hash_password(password))
        self.create_user(user)
        return user
