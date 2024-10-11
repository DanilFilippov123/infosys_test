from db.models.session_dto import SessionDTO


class SessionRepository:

    def save(self, session: SessionDTO) -> SessionDTO:
        pass

    def load(self, key: str) -> SessionDTO:
        pass

    def delete(self, key: str) -> None:
        pass
