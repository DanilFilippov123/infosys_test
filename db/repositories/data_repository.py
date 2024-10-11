from db.models.data_dto import DataDTO
from db.orm.data_orm import DataModel
from db.repositories.base import Repository
from db.session import Session


class DataRepository(Repository[DataModel, DataDTO]):

    def save(self, data: DataDTO) -> DataDTO:
        data_orm = DataModel(key=data.key, data=data.data)
        with Session() as session:
            session.add(data_orm)
            session.commit()
        return data

    def load(self, key: str) -> DataDTO:
        with Session() as session:
            data_orm = session.get_one(DataModel, DataModel.key == key)
        return self.mapper_to_dto(data_orm)

    @staticmethod
    def mapper_to_dto(user_orm: DataModel) -> DataDTO:
        return DataDTO(key=user_orm.key, data=user_orm.data)

    def delete(self, key) -> None:
        with Session() as session:
            session.delete(session.get_one(DataModel, DataModel.key == key))
            session.commit()
