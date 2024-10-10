import datetime
from dataclasses import dataclass

@dataclass
class SessionDTO:
    key: str
    expired_at: datetime.datetime
    challenge: str
    secret: str
