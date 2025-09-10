from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from typing import Dict, Any


class Base(DeclarativeBase):
    pass

class User(Base):
    """Класс для описания пользователей"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))


    def __repr__(self):
        return (f"User(id = {self.id}, name = {self.name}, surname = {self.surname}, email = {self.email})")


    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

