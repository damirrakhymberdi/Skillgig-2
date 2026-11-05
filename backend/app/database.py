import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .core.config import get_settings

settings = get_settings()

connect_args = {}
database_url = settings.database_url

if database_url.startswith("postgres://"):
    database_url = "postgresql+psycopg://" + database_url[len("postgres://") :]
elif database_url.startswith("postgresql://"):
    database_url = "postgresql+psycopg://" + database_url[len("postgresql://") :]

if database_url.startswith("sqlite"):
    db_path = database_url.replace("sqlite:///", "", 1)
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    # On some filesystems (especially bind mounts on Windows/macOS), SQLite can be flaky.
    # A small timeout makes it more resilient under concurrent access.
    connect_args = {"check_same_thread": False, "timeout": 30}

engine = create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

