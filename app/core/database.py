from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create async engine for SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Create a base class for all models
Base = declarative_base()

async def get_db():
    """
    Dependency function to get a database session.
    
    Yields:
        AsyncSession: SQLAlchemy async session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 