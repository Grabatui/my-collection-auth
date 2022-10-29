import hashlib
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    source = Column(String, nullable=False)
    inserted_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def check_password(self, password: str, salt: str) -> bool:
        check_password = self.__make_hash_from_password(password, salt)

        return self.password == check_password

    def __make_hash_from_password(self, password: str, salt: str) -> str:
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
