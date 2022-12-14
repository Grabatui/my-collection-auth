from typing import Optional
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.core.persistence.entity import User


class Database:
    def __init__(self, database_string: str) -> None:
        self.engine = create_engine(database_string)
        self.session = sessionmaker(self.engine, expire_on_commit=False)


class AbstractRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def _insert_entity(self, entity) -> None:
        with self.database.session() as session:
            session.add(entity)
            session.commit()


class UserRepository(AbstractRepository):
    def insert(self, user: User) -> None:
        self._insert_entity(user)

    def get_by_username(self, username: str) -> Optional[User]:
        with self.database.session() as session:
            return session.query(User).filter_by(username=username).first()

    def is_username_exists(self, username: str) -> bool:
        return self.get_by_username(username) is not None
