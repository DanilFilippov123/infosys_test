class SessionError(Exception):
    pass


class SessionExpired(SessionError):
    pass


class NoSessionError(SessionError):
    pass
