from sqlalchemy.orm import Mapped, mapped_column

from db.orm.base_orm import Base


class DataModel(Base):
    __tablename__ = "data"

    key: Mapped[str] = mapped_column(primary_key=True)

    data: Mapped[str] = mapped_column()
