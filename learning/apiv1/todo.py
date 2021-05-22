from typing import List

from aiologger import Logger  # type: ignore
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from learning.entities import Todo

from ..repositories import TodoRepository
from ..schemas import CreateTodo, TodoItem
from .dependencies import session_context

logger = Logger.with_default_handlers(name=__file__)

todo_router = APIRouter(prefix="/todos")
repo = TodoRepository()


@todo_router.get("", response_model=List[TodoItem])
async def get_todos(session: AsyncSession = Depends(session_context)):
    todos = await repo.get_todos(session)
    return todos


@todo_router.post("", response_model=TodoItem, status_code=201)
async def creat_todo(new_todo: CreateTodo, session: AsyncSession = Depends(session_context)):
    todo = Todo(new_todo.title)
    todo = await repo.create_todo(todo, session)
    return todo


@todo_router.put("/{id}", response_model=TodoItem)
async def update_todo(id: int, todo: CreateTodo, session: AsyncSession = Depends(session_context)):
    todo = await repo.update_todo(id, todo, session)
    return todo


@todo_router.put("/{id}/done", response_model=TodoItem)
async def done(id: int, session: AsyncSession = Depends(session_context)):
    todo = await repo.done(id, session)
    return todo


@todo_router.delete("/{id}", status_code=204)
async def delete_todo(id: int, session: AsyncSession = Depends(session_context)):
    await repo.delete(id, session)
    return None
