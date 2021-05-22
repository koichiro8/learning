from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from learning.errors import TitleLengthError

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    done = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)

    def __init__(self, title: str):
        self.title = self.check_title(title)

    def check_title(self, title: str):
        length = len(title)
        if not (0 < length < 257):
            raise TitleLengthError(f"title length is not between 1 and 256, length: {length}")
        return title

    def __repr__(self) -> str:
        return f"<Todo(id={self.id}, title={self.title}, done={self.done}, created_at={self.created_at})>"
