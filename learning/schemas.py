from datetime import datetime

from pydantic import BaseModel


class TodoItem(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime

    class Config:
        orm_mode = True


class CreateTodo(BaseModel):
    title: str
