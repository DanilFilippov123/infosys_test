class AuthenticationError(Exception):
    pass


class InvalidPassword(AuthenticationError):
    pass
