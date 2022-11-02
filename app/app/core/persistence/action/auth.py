from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token

from app.core.persistence.repository import UserRepository
from app.core.domain.auth.entity import Tokens
from app.core.domain.auth import AreAuthorizeCredentialsCorrectInterface, GenerateAccessAndRefreshTokensInterface


class AreAuthorizeCredentialsCorrectAction(AreAuthorizeCredentialsCorrectInterface):
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def run(self, username: str, encodedPassword: str) -> bool:
        user = self.userRepository.get_by_username(username)

        if not user or user.password != encodedPassword:
            return False

        return True


class GenerateAccessAndRefreshTokensAction(GenerateAccessAndRefreshTokensInterface):
    def __init__(self, jwtAccessTokenExpiresIn: int, jwtRefreshTokenExpiresIn: int):
        self.accessTokenExpiresIn = jwtAccessTokenExpiresIn
        self.refreshTokenExpiresIn = jwtRefreshTokenExpiresIn

    def run(self, username: str) -> Tokens:
        accessToken = create_access_token(
            identity=username,
            expires_delta=timedelta(seconds=self.accessTokenExpiresIn)
        )
        refreshToken = create_refresh_token(
            identity=username,
            expires_delta=timedelta(seconds=self.refreshTokenExpiresIn)
        )

        return Tokens(accessToken, refreshToken, self.accessTokenExpiresIn)
