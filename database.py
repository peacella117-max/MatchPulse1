from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from bot.config import config
from bot.models.user import Base

# Async engine
async_engine = create_async_engine(
    config.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://'),
    echo=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Initialize database"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session
