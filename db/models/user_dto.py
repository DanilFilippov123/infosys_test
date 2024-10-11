from dataclasses import dataclass


@dataclass
class UserDTO:
    login: str
    password: str

    session_key: str | None = None
