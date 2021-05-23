import os

from ward import fixture

from learning.database import get_enigne, initialize_session
from learning.entities import Base


@fixture
async def db_session():
    engine = get_enigne(os.environ["TEST_DB_URL"])
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    initialize_session(engine)
