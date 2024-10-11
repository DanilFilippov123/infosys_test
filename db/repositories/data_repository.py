from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from db.models.data_dto import DataDTO
from db.orm.data_orm import DataModel
from db.repositories.base import Repository
from db.session import Session
from errors.data_errors import NoDataError


class DataRepository(Repository[DataModel, DataDTO]):

    def save(self, data: DataDTO) -> DataDTO:
        data_orm = DataModel(key=data.key,
                             data=data.data)
        with Session() as session:
            session.add(data_orm)
            prev_data = session.execute(select(DataModel)
                                        .where(DataModel.key == data_orm.key)
                                        ).scalar_one_or_none()
            if prev_data is None:
                session.add(data_orm)
            else:
                data_orm = session.merge(data_orm)
            session.commit()
            result = self.mapper_to_dto(data_orm)
            session.commit()
        return result

    def load(self, key: str) -> DataDTO:
        try:
            with Session() as session:
                data_orm = session.get_one(DataModel, key)
                result = self.mapper_to_dto(data_orm)
        except NoResultFound:
            raise NoDataError("No data found")
        return result

    @staticmethod
    def mapper_to_dto(user_orm: DataModel) -> DataDTO:
        return DataDTO(key=user_orm.key, data=user_orm.data)

    def delete(self, key) -> None:
        with Session() as session:
            session.delete(session.get_one(DataModel, DataModel.key == key))
            session.commit()
