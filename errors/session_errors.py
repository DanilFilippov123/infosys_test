class SessionError(Exception):
    pass


class SessionExpired(SessionError):
    pass
