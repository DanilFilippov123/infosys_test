import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.orm.base_orm import Base


class SessionModel(Base):
    __tablename__ = "session"

    key: Mapped[str] = mapped_column(primary_key=True,
                                     default=lambda: uuid.uuid4().hex)

    secret: Mapped[int] = mapped_column(nullable=True)
    challenge: Mapped[str] = mapped_column(nullable=True)

    expired_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="session")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
