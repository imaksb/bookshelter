from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.infrastructure.models.base import Base


def create_engine():
    return create_async_engine(settings.sqlalchemy_database_uri,
                               future=True)


async def create_session_pool():
    engine = create_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_pool = async_sessionmaker(bind=engine,
                                      expire_on_commit=False)
    return session_pool
