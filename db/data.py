from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"author(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))
    nick_name: Mapped[str] = Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"account(id={self.id!r}, name={self.user_name!r}, nick_name={self.nick_name!r})"


class Opus(Base):
    __tablename__ = "opus"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    author_id: Mapped[int]
    account_id: Mapped[int]
    downloaded: Mapped[int]
    published: Mapped[int]
    page_index: Mapped[int]

    def __repr__(self) -> str:
        return f"Opus(id={self.id!r}, code={self.code!r})"
