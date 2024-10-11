from db.models.data_dto import DataDTO


class DataRepository:

    def __init__(self) -> None:
        pass

    def save(self, data: DataDTO) -> DataDTO:
        pass

    def load(self, key: str) -> DataDTO:
        pass
