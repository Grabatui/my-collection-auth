from flask_jwt_extended import get_jwt_identity

from app.core.domain.auth.entity import Tokens


class AreAuthorizeCredentialsCorrectInterface():
    def run(self, username: str, encodedPassword: str) -> bool:
        raise Exception('Method must be implemented')


class GenerateAccessAndRefreshTokensInterface():
    def run(self, username: str) -> Tokens:
        raise Exception('Method must be implemented')


class AuthorizedIdentityProvider():
    def run(self) -> str:
        return get_jwt_identity()
