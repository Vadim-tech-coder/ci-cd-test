from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY, ForeignKey, Integer
from typing import Dict, Any
from sqlalchemy.dialects.postgresql import TSVECTOR, JSON



class Base(DeclarativeBase):
    pass

class Coffee(Base):
    __tablename__ = 'coffee'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(String(200))
    search_vector = mapped_column(TSVECTOR)
    category:Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    reviews: Mapped[str] = mapped_column(ARRAY(String), nullable=True)
    user: Mapped["User"] = relationship(back_populates="coffee")

    def __repr__(self):
        return (f"Coffee: id = {self.id}, title = {self.title}, origin = {self.description}, "
                f"intensifier = {self.category}, notes = {self.reviews}")


    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    has_sale: Mapped[bool | None]
    address: Mapped[dict | None] = mapped_column(JSON)
    search_vector = mapped_column(TSVECTOR)
    coffee_id: Mapped[int | None] = mapped_column(ForeignKey("coffee.id"))
    coffee: Mapped["Coffee"] = relationship(back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name})"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


