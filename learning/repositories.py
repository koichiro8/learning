from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete

from learning.errors import NotFoundError
from learning.schemas import CreateTodo

from .entities import Todo


class TodoRepository:
    async def get_todos(self, session: AsyncSession):
        result = await session.execute(select(Todo).order_by(Todo.created_at))
        return result.scalars().all()

    async def create_todo(self, todo: Todo, session: AsyncSession):
        async with session.begin():
            session.add(todo)
        return todo

    async def update_todo(self, id: int, new_todo: CreateTodo, session: AsyncSession):
        result = await session.execute(select(Todo).filter(Todo.id == id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise NotFoundError(f"id: {id} is not found")

        todo.title = new_todo.title
        return todo

    async def done(self, id: int, session: AsyncSession):
        result = await session.execute(select(Todo).filter(Todo.id == id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise NotFoundError(f"id: {id} is not found")

        todo.done = False if todo.done else True
        return todo

    async def delete(self, id: int, session: AsyncSession):
        await session.execute(delete(Todo).filter(Todo.id == id))
