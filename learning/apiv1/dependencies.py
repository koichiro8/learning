from aiologger import Logger  # type: ignore

from ..database import get_session

logger = Logger.with_default_handlers(name=__file__)


async def session_context():
    async with get_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as ex:
            await logger.exception(ex)
            await session.rollback()
