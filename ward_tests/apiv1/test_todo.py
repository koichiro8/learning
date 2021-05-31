from ward import test

from learning.database import get_session

from ..fixtures import api_test_client, db_session
from ..utils import create_todo


@test("get todos", tags=["integration"])
async def _(api_test_client=api_test_client, db_session=db_session):
    todos = create_todo(5)
    async with get_session() as session:
        async with session.begin():
            session.add_all(todos)

        await session.commit()

    async with api_test_client as ac:
        res = await ac.get("/todos")
    assert res.status_code == 200
    assert len(res.json()) == 5
    for todo in res.json():
        assert "id" in todo
        assert "title" in todo
        assert "done" in todo
        assert "created_at" in todo


@test("create todo", tags=["integration"])
async def _(api_test_client=api_test_client, db_session=db_session):
    async with api_test_client as ac:
        res = await ac.post("/todos", json={"title": "test todo"})
    assert res.status_code == 201
    created = res.json()
    assert created["title"] == "test todo"
