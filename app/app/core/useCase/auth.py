from app.core.domain.common import EncodePasswordInterface
from app.core.domain.auth import AreAuthorizeCredentialsCorrectInterface, GenerateAccessAndRefreshTokensInterface
from app.core.domain.auth.entity import Tokens


class AuthorizeWithCredentialsUseCase():
    def __init__(
        self,
        encodePassword: EncodePasswordInterface,
        areAuthorizeCredentialsCorrect: AreAuthorizeCredentialsCorrectInterface,
        generateAccessAndRefreshTokens: GenerateAccessAndRefreshTokensInterface
    ):
        self.encodePassword = encodePassword
        self.areAuthorizeCredentialsCorrect = areAuthorizeCredentialsCorrect
        self.generateAccessAndRefreshTokens = generateAccessAndRefreshTokens

    def run(self, username: str, decodedPassword: str, source: str) -> Tokens:
        encodedPassword = self.encodePassword.run(decodedPassword)

        if not self.areAuthorizeCredentialsCorrect.run(username, encodedPassword, source):
            raise Exception('Credentials are wrong')

        return self.generateAccessAndRefreshTokens.run(username)
