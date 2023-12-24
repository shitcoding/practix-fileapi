from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from models.file_properties import SQLModel

from core.config import settings

db_engine = create_async_engine(
    settings.db.url,
    echo=settings.debug,
    future=True,
)

async_session = sessionmaker(
    db_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Create database tables."""
    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """Create async db session."""
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
