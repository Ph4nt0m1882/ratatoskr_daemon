import sqlite3
import sqlite_vec
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os

from app.db import models
from app.core.config import settings




def get_database() -> tuple[str, str]:
    """Get the database URL for the SQLite database.

    Returns:
        tuple[str, str]: A tuple containing the db_name and db_url.
    """
    method = settings.db_access_method
    os.makedirs(settings.settings_folder, exist_ok=True)
    
    if method.value == "local":
        db_name = os.path.join(settings.settings_folder, f"{settings.database_name}.toskr")
        db_url = f"sqlite:///{db_name}"
    else:
        db_name = "fallback.toskr"
        db_url = f"sqlite:///{db_name}"

    return db_name, db_url

DATABASE_NAME, DATABASE_URL = get_database()
    

def _create_sqlite_connection() -> sqlite3.Connection:
    """Create a raw SQLite connection and load the sqlite-vec extension.

    This function is used as a custom creator for the SQLAlchemy engine,
    ensuring that every connection to the database has the vector capabilities
    loaded and ready to use for RAG.

    Returns:
        sqlite3.Connection: A database connection with sqlite-vec loaded.
    """
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn

## create_engine is the core of SQLModel (and SQLAlchemy)
## We use our custom creator to inject sqlite-vec
engine = create_engine(
    DATABASE_URL,
    echo=True,
    creator=_create_sqlite_connection,
    poolclass=StaticPool
)

def create_db_and_tables() -> None:
    """Create the database and all tables based on the defined SQLModels.
    
    This function should be called on application startup.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency injection for FastAPI to get a database session per request.

    Yields:
        Session: A SQLModel database session.
    """
    with Session(engine) as session:
        yield session



