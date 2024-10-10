from dataclasses import dataclass

import config


@dataclass
class UserDTO:
    login: str
    password: str
    def __post_init__(self):
        if len(self.login) > config.max_login_length:
            ValueError("login too long!")
        if len(self.password) > config.max_password_length:
            ValueError("password too long!")



