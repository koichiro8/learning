from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def get_enigne(db_url):
    engine = create_async_engine(
        db_url,
        echo=True,
    )
    return engine


async_session = None


def initialize_session(engine: AsyncEngine):
    global async_session
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_session():
    global async_session
    return async_session()  # type: ignore
