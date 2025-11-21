from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.db import engine, init_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    from sqlmodel import Session
    with Session(engine) as session:
        init_db(session)
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
