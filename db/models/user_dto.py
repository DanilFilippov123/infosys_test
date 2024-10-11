from dataclasses import dataclass
from typing import Any


@dataclass
class UserDTO:
    login: str
    password: str

    id_: int | None = None
    session: Any | None = None
