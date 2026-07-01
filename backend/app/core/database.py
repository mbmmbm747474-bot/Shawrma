from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

_is_sqlite = settings.DATABASE_URL.startswith("sqlite")

_engine_kwargs = {
    "echo": settings.DEBUG,
    "future": True,
}

if _is_sqlite:
    # SQLite's pool doesn't accept pool_size/max_overflow, and the default
    # driver is single-threaded per connection unless told otherwise - the
    # desktop app talks to it from FastAPI's threadpool, so allow that.
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    _engine_kwargs.update(
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=40,
    )

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)

if _is_sqlite:
    # SQLite ignores FOREIGN KEY constraints unless explicitly turned on
    # per-connection - this schema relies on them, so enable it everywhere.
    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
