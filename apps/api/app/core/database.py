"""
Database configuration and session management
"""

import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import MetaData

from app.core.config import settings

# Database URL conversion for async
def get_async_database_url() -> str:
    """Convert PostgreSQL URL to async format"""
    if settings.DATABASE_URL.startswith("postgresql://"):
        return settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    return settings.DATABASE_URL

# Create async engine
engine = create_async_engine(
    get_async_database_url(),
    echo=settings.DEBUG,
    poolclass=NullPool if settings.DEBUG else None,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Import all models to ensure they are registered
        from app.models import user, listing, booking, review, message, transaction
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Create indexes
        await conn.run_sync(create_indexes)


def create_indexes(metadata):
    """Create database indexes"""
    from sqlalchemy import Index, text
    
    # Create spatial index for listings
    metadata.create_all(engine, checkfirst=True)
    
    # Create additional indexes
    with engine.connect() as conn:
        # Spatial index for PostGIS
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_listings_geog 
            ON listings USING GIST (geog);
        """))
        
        # Full-text search index
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_listings_search 
            ON listings USING GIN (to_tsvector('english', title || ' ' || description));
        """))
        
        # Composite indexes for common queries
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_listings_city_type 
            ON listings (city, type, status);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_bookings_dates_status 
            ON bookings (check_in, check_out, status);
        """))
        
        conn.commit()


async def close_db() -> None:
    """Close database connections"""
    await engine.dispose()


# Test database functions
async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    """Get test database session"""
    if not settings.DATABASE_TEST_URL:
        raise ValueError("Test database URL not configured")
    
    test_engine = create_async_engine(
        settings.DATABASE_TEST_URL.replace("postgresql://", "postgresql+asyncpg://", 1),
        echo=False,
        poolclass=NullPool,
    )
    
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    async with TestSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            await test_engine.dispose()


async def init_test_db() -> None:
    """Initialize test database"""
    if not settings.DATABASE_TEST_URL:
        raise ValueError("Test database URL not configured")
    
    test_engine = create_async_engine(
        settings.DATABASE_TEST_URL.replace("postgresql://", "postgresql+asyncpg://", 1),
        echo=False,
        poolclass=NullPool,
    )
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    await test_engine.dispose()
