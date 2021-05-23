import asyncio
import os

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine

from learning.database import get_enigne, initialize_session
from learning.entities import Base


async def initialize_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
def db_session():
    engine = get_enigne(os.environ["TEST_DB_URL"])
    asyncio.run(initialize_db(engine))
    initialize_session(engine)
