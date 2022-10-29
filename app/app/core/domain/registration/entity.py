from enum import Enum


class SourceEnum(Enum):
    movies = 'movies'


class NewUser():
    def __init__(
        self,
        username: str,
        encodedPassword: str,
        source: SourceEnum
    ):
        self.username = username
        self.encodedPassword = encodedPassword
        self.source = source

    def __repr__(self) -> str:
        return f'User(username={self.username}, source={self.source!r})'
