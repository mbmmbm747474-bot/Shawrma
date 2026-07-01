import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db
from app.models.base import Base

# Models use a portable GUID/JSON type (app/models/types.py) that adapts
# to whichever database engine is connected - real UUID/JSONB on Postgres,
# plain CHAR(36)/JSON on SQLite (used by the desktop build, see
# DESKTOP_BUILD.md). These integration tests specifically exercise the
# Postgres path since that's the real deployment target; point
# TEST_DATABASE_URL at a throwaway database - never run these against
# production data, since every table is dropped and recreated per test.
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/restaurant_erp_test",
)


@pytest.fixture(scope="function")
def db_session():
    """Isolated Postgres session for each test.

    Creates all tables before the test and drops them after, so each test
    starts from a clean schema. Requires a running Postgres instance at
    TEST_DATABASE_URL (defaults to a local `restaurant_erp_test` database;
    override the env var to point elsewhere, e.g. the docker-compose
    `postgres` service).
    """
    engine = create_engine(TEST_DATABASE_URL, future=True)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover - environment guard
        pytest.skip(
            f"Postgres test database not reachable at {TEST_DATABASE_URL} "
            f"({exc}). Set TEST_DATABASE_URL or start the docker-compose "
            f"postgres service to run these tests."
        )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def client(db_session):
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
