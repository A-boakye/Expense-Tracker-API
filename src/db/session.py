from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .base import Base
from ..config import settings


engine = create_async_engine(url=settings.DATABASE_URL)

AsyncSessionLocal=async_sessionmaker(bind=engine, class_=AsyncSession)



async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

