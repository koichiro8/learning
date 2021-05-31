import os

from httpx import AsyncClient
from ward import fixture

from learning.app import create_app
from learning.database import get_enigne, initialize_session
from learning.entities import Base


@fixture
async def db_session():
    engine = get_enigne(os.environ["TEST_DB_URL"])
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    initialize_session(engine)


@fixture(scope="global")
def api_test_client():
    return AsyncClient(app=create_app(os.environ["TEST_DB_URL"]), base_url="http://test")
