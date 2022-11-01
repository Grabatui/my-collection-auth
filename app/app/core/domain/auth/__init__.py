from app.core.domain.auth.entity import Tokens


class AreAuthorizeCredentialsCorrectInterface():
    def run(self, username: str, encodedPassword: str, source: str) -> bool:
        raise Exception('Method must be implemented')


class GenerateAccessAndRefreshTokensInterface():
    def run(self, username: str) -> Tokens:
        raise Exception('Method must be implemented')
