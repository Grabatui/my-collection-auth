from typing import Optional
import re

from app.core.domain.registration.entity import NewUser, SourceEnum


PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 20
PASSWORD_MASK_LETTERS = 'a-zA-Z'
PASSWORD_MASK_NUMBERS = '0-9'
PASSWORD_MASK_SYMBOLS = '`~!@#$%^&*()_\-+={}[\]\\|:;"\'<>,.?/'


class ConvertSourceTokenInterface():
    def run(self, raw_token: str) -> str:
        raise Exception('Method must be implemented')


class EncodePasswordInterface():
    def run(self, decodedPassword: str) -> str:
        raise Exception('Method must be implemented')


class CreateUserInterface():
    def run(self, user: NewUser) -> bool:
        raise Exception('Method must be implemented')


class IsUsernameAlreadyExistsInterface():
    def run(self, username: str) -> bool:
        raise Exception('Method must be implemented')


class SourceTokensProvider():
    def __init__(
        self,
        tokensBySources: dict,
        convertSourceToken: ConvertSourceTokenInterface
    ) -> None:
        self.tokensBySources = tokensBySources
        self.convertSourceToken = convertSourceToken

    def get(self, token: str) -> Optional[str]:
        formattedToken = self.convertSourceToken.run(token)

        for source, checkToken in self.tokensBySources.items():
            if checkToken == formattedToken:
                return source

        return None


class UserFactory():
    def __init__(self, encodePassword: EncodePasswordInterface):
        self.encodePassword = encodePassword

    def make(self, source: str, username: str, password: str) -> NewUser:
        return NewUser(
            username=username,
            encodedPassword=self.encodePassword.run(password),
            source=SourceEnum[source]
        )


class PasswordValidator():
    def run(self, password: str) -> tuple:
        errors = []

        if len(password) < PASSWORD_MIN_LENGTH:
            errors.append('Password is shorter than ' + str(PASSWORD_MIN_LENGTH))
        elif len(password) > PASSWORD_MAX_LENGTH:
            errors.append('Password is longer than ' + str(PASSWORD_MAX_LENGTH))

        lettersPattern = re.compile('[' + PASSWORD_MASK_LETTERS + ']')
        numbersPattern = re.compile('[' + PASSWORD_MASK_NUMBERS + ']')
        symbolsPattern = re.compile('[' + PASSWORD_MASK_SYMBOLS + ']')

        if (
            not lettersPattern.search(password)
            or not numbersPattern.search(password)
            or not symbolsPattern.search(password)
        ):
            errors.append(
                'Password must contains: latin letters, numbers and at least one of ' + ', '.join(list(PASSWORD_MASK_SYMBOLS))
            )

        return len(errors) <= 0, errors
