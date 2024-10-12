import datetime
import uuid
from dataclasses import dataclass


@dataclass
class SessionDTO:
    expired_at: datetime.datetime
    user: "UserDTO"

    challenge: str | None = None
    secret: int | None = None

    key: str | None = None
