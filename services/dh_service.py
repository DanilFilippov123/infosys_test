import secrets


class DHService:

    def __init__(self, prime: int, generator: int) -> None:
        self.prime = prime
        self.generator = generator

    def get_public_keys(self) -> tuple[int, int]:
        return self.prime, self.generator

    @staticmethod
    def generate_private_key() -> int:
        return secrets.randbits(16)

    def generate_partial_key(self, pk: int) -> int:
        return pow(self.generator, pk, self.prime)

    def generate_full_key(self,
                          partial_key: int,
                          pk: int):
        return pow(partial_key, pk, self.prime)
