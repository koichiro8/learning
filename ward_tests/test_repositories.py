from datetime import datetime

from sqlalchemy import select
from ward import test

from learning.database import get_session
from learning.entities import Todo
from learning.repositories import TodoRepository
from learning.schemas import CreateTodo
from ward_tests.fixtures import db_session


def create_todo(cnt: int):
    return [Todo(title=f"todo no.{i}") for i in range(cnt)]


@test("get todos", tags=["integration"])
async def _(db_session=db_session):
    todos = create_todo(5)
    repo = TodoRepository()
    async with get_session() as session:
        async with session.begin():
            session.add_all(todos)

        await session.commit()

        got = await repo.get_todos(session)

    assert len(got) == 5


@test("create todo", tags=["integration"])
async def _(db_session=db_session):
    now = datetime.now()
    repo = TodoRepository()
    async with get_session() as session:
        await repo.create_todo(Todo("create todo"), session)
        await session.commit()

        result = await session.execute(select(Todo))
        created: Todo = result.scalar_one_or_none()

    assert created
    assert created.title == "create todo"
    assert not created.done
    assert created.created_at >= now


@test("update todo", tags=["integration"])
async def _(db_session=db_session):
    repo = TodoRepository()
    async with get_session() as session:
        await repo.create_todo(Todo("create todo"), session)
        await session.commit()

        result = await session.execute(select(Todo))
        created: Todo = result.scalar_one_or_none()

    async with get_session() as session:
        await repo.update_todo(created.id, CreateTodo(title="update todo"), session)
        await session.commit()
        result = await session.execute(select(Todo))
        updated: Todo = result.scalar_one_or_none()

    assert updated
    assert updated.title == "update todo"
    assert not updated.done
    assert updated.created_at == created.created_at


@test("done", tags=["integration"])
async def _(db_session=db_session):
    repo = TodoRepository()
    async with get_session() as session:
        await repo.create_todo(Todo("create todo"), session)
        await session.commit()

        result = await session.execute(select(Todo))
        created: Todo = result.scalar_one_or_none()

    async with get_session() as session:
        await repo.done(created.id, session)
        await session.commit()
        result = await session.execute(select(Todo))
        done: Todo = result.scalar_one_or_none()

    assert done
    assert done.title == "create todo"
    assert done.done
    assert done.created_at == created.created_at


@test("delete", tags=["integration"])
async def _(db_session=db_session):
    repo = TodoRepository()
    async with get_session() as session:
        await repo.create_todo(Todo("create todo"), session)
        await session.commit()

        result = await session.execute(select(Todo))
        created: Todo = result.scalar_one_or_none()

    async with get_session() as session:
        await repo.delete(created.id, session)
        result = await session.execute(select(Todo))
        deleted: Todo = result.scalar_one_or_none()

    assert not deleted


@test("delete done", tags=["integration"])
async def _(db_session=db_session):
    todos = create_todo(5)
    repo = TodoRepository()
    async with get_session() as session:
        async with session.begin():
            session.add_all(todos)

        await session.commit()

        result = await session.execute(select(Todo))
        created: Todo = result.scalars().all()

    done_ids = [created[1].id, created[3].id]

    async with get_session() as session:
        for done_id in done_ids:
            await repo.done(done_id, session)
        await session.commit()

    async with get_session() as session:
        await repo.delete_done(session)
        await session.commit()

        result = await session.execute(select(Todo))
        not_doned: Todo = result.scalars().all()

    assert len(not_doned) == 3
    not_doned_ids = [d.id for d in not_doned]
    for done_id in done_ids:
        assert done_id not in not_doned_ids
