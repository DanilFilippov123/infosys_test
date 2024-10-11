import abc


class Repository[Model, DTO](abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def mapper_to_dto(user_orm: Model) -> DTO:
        pass

    @abc.abstractmethod
    def save(self, obj: T) -> T:
        pass

    @abc.abstractmethod
    def load(self, key) -> T:
        pass

    @abc.abstractmethod
    def delete(self, key) -> None:
        pass
