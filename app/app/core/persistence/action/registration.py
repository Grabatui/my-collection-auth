from app.core.domain.registration import CreateUserInterface, IsUsernameAlreadyExistsInterface
from app.core.persistence.repository import UserRepository
from app.core.domain.registration.entity import NewUser
from app.core.persistence.model.registration import NewUserModel


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
