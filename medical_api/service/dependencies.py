from typing import Generator, Optional

from loguru import logger
from sqlalchemy.orm import Session as SessionType

from database import async_session


async def get_db() -> Generator[SessionType, None, None]:  # pragma: no cover
    db: Optional[SessionType] = None
    try:
        async with async_session() as db:
            yield db
            try:
                await db.commit()
            except:  # pylint: disable=bare-except
                logger.exception("Could not commit transaction on end of request!")
                await db.rollback()
    except Exception as e:  # pylint: disable=bare-except
        logger.exception("Could not create db session!")
