from binascii import hexlify
from hashlib import sha256, pbkdf2_hmac

from app.core.domain.registration import ConvertSourceTokenInterface, CreateUserInterface, EncodePasswordInterface, IsUsernameAlreadyExistsInterface
from app.core.persistence.repository import UserRepository
from app.core.domain.registration.entity import NewUser
from app.core.persistence.model.registration import NewUserModel


class ConvertSourceTokenAction(ConvertSourceTokenInterface):
    def run(self, raw_token: str) -> str:
        return sha256(raw_token.encode('utf-8')).hexdigest()


class EncodePasswordAction(EncodePasswordInterface):
    def __init__(self, salt: str):
        self.salt = salt

    def run(self, decodedPassword: str) -> str:
        encodedPassword = pbkdf2_hmac(
            'sha256',
            decodedPassword.encode('utf-8'),
            self.salt.encode('utf-8'),
            100000
        )

        return hexlify(encodedPassword).decode('utf-8')


class CreateUserAction(CreateUserInterface):
    def __init__(self, userRepository: UserRepository, newUserModel: NewUserModel):
        self.userRepository = userRepository
        self.newUserModel = newUserModel

    def run(self, user: NewUser) -> bool:
        self.userRepository.insert(
            self.newUserModel.fromNewUserToUser(user)
        )

        return True


class IsUsernameAlreadyExistsAction(IsUsernameAlreadyExistsInterface):
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def run(self, username: str) -> bool:
        return self.userRepository.is_username_exists(username)
