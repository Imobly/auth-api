import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

use_nullpool = os.getenv("DB_USE_NULLPOOL", "true").lower() == "true" or \
    ("supabase.com" in settings.DATABASE_URL and ":6543" in settings.DATABASE_URL)

if use_nullpool:
    engine = create_engine(settings.DATABASE_URL, poolclass=NullPool, pool_pre_ping=True, echo=settings.DEBUG)
else:
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    import app.src.auth.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
