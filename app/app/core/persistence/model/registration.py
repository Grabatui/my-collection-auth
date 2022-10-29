import datetime

from app.core.domain.registration.entity import NewUser
from app.core.persistence.entity import User


class NewUserModel():
    def fromNewUserToUser(self, domainEntity: NewUser) -> User:
        now = datetime.datetime.utcnow()

        return User(
            username=domainEntity.username,
            password=domainEntity.encodedPassword,
            source=domainEntity.source.value,
            inserted_at=now,
            updated_at=now
        )
