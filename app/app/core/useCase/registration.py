from app.core.domain.registration import CreateUserInterface, UserFactory


class RegisterUseCase():
    def __init__(self, userFactory: UserFactory, createUser: CreateUserInterface):
        self.userFactory = userFactory
        self.createUser = createUser

    def run(self, source: str, username: str, password: str) -> bool:
        user = self.userFactory.make(source, username, password)

        return self.createUser.run(user)
