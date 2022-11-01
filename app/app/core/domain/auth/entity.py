class Tokens():
    def __init__(
        self,
        accessToken: str,
        refreshToken: str,
        expiresIn: int
    ):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.expiresIn = expiresIn
