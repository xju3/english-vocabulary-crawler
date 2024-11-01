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
    id = Column(Integer, primary_key=True)
    code = Column(String)
    author_id = Column(Integer)
    account_id = Column(Integer)
    downloaded = Column(Integer)
    published = Column(Integer)
    page_index = Column(Integer)