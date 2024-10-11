from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.orm.base_orm import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    session: Mapped["SessionModel"] = relationship(back_populates="user")
