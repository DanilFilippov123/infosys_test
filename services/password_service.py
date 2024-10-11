import hashlib
import secrets


class PasswordService:

    hashing_functions_mapping = {
        "sha256": lambda x: hashlib.sha256(x.encode()).hexdigest(),
    }

    def __init__(self,
                 salt_lenght: int = None,
                 hash_method: str = "sha256") -> None:
        self._salt_length = salt_lenght
        self._hash_method_name = hash_method
        self.hash_function = self.hashing_functions_mapping[self._hash_method_name]

    def hash_password(self, password: str) -> str:
        """
        Функция хеширования пароля. Возварщает хэшированный пароль в виде <алгоритм>$<хэш>$<соль>
        """
        salt = self.gen_salt()
        hashed_password = self.hash_function(f"{password}${salt}")
        return f"{self._hash_method_name}${hashed_password}${salt}"

    def gen_salt(self) -> str:
        return secrets.token_hex(self._salt_length)

    def check_password(self, password: str, hashed_password: str) -> bool:
        """
        Функция проверки пароля. Возвращает True если пароль совпадает, иначе False
        """
        method_name, hashed_password, salt = hashed_password.split("$")
        method = self.hash_function[method_name]
        return method(f"{password}${salt}") == hashed_password
