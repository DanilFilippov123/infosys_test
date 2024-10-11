import hmac


class UserSignatureService:

    def __init__(self, hashing_method="sha256") -> None:
        self.hashing_method = hashing_method

    def validate_signature(self,
                           signature: str,
                           challenge: str,
                           secret: int) -> bool:
        current_sig = hmac.new(key=secret.to_bytes(),
                               msg=challenge.encode(),
                               digestmod=self.hashing_method).hexdigest()
        return current_sig == signature

