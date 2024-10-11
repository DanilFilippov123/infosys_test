import secrets


class ChallengeService:
    def __init__(self, length=32) -> None:
        self._length = length

    def get_challenge(self) -> str:
        return secrets.token_hex(self._length)
