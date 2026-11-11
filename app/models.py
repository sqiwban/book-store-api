import enum
from datetime import date, datetime

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text)
    birth_date: Mapped[date]

    books: Mapped[list["Book"]] = relationship(back_populates="author", lazy="selectin")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    stock_quantity: Mapped[int] = mapped_column(default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    author: Mapped["Author"] = relationship(back_populates="books", lazy="joined")

    __table_args__ = (Index("ix_books_author_id", "author_id"),)