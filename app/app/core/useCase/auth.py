from app.core.domain.common import EncodePasswordInterface
from app.core.domain.auth import AreAuthorizeCredentialsCorrectInterface, AuthorizedIdentityProvider, GenerateAccessAndRefreshTokensInterface
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

    def run(self, username: str, decodedPassword: str) -> Tokens:
        encodedPassword = self.encodePassword.run(decodedPassword)

        if not self.areAuthorizeCredentialsCorrect.run(username, encodedPassword):
            raise Exception('Credentials are wrong')

        return self.generateAccessAndRefreshTokens.run(username)


class RefreshTokenUseCase():
    def __init__(
        self,
        authorizedIdentityProvider: AuthorizedIdentityProvider,
        generateAccessAndRefreshTokens: GenerateAccessAndRefreshTokensInterface
    ):
        self.authorizedIdentityProvider = authorizedIdentityProvider
        self.generateAccessAndRefreshTokens = generateAccessAndRefreshTokens

    def run(self) -> Tokens:
        username = self.authorizedIdentityProvider.run()

        return self.generateAccessAndRefreshTokens.run(username)
