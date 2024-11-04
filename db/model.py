from typing import Optional

from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self) -> str:
        return f"author(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    nick_name = Column(String)

    def __repr__(self) -> str:
        return f"account(id={self.id!r}, name={self.user_name!r}, nick_name={self.nick_name!r})"


class Opus(Base):
    __tablename__ = "opus"
    id: Mapped[str] = mapped_column(primary_key=True)
    code : Mapped[str] = mapped_column()
    words : Mapped[str] = mapped_column()
    prose : Mapped[str] = mapped_column()
    author_id : Mapped[int] = mapped_column()
    account_id : Mapped[int] = mapped_column()
    downloaded : Mapped[int] = mapped_column()
    published : Mapped[int] = mapped_column()
    page_index : Mapped[int] = mapped_column()
    extracted: Mapped[int] = mapped_column()
    err :Mapped[int] = mapped_column()
