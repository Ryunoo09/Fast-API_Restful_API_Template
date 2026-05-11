import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.core.rate_limit import limiter
from app.main import app

limiter.enabled = False

from sqlalchemy.pool import StaticPool

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    
    # Patch init_db so it doesn't run and connect to the real database
    from unittest.mock import patch
    with patch("app.main.init_db"):
        with TestClient(app) as c:
            yield c
            
    app.dependency_overrides.clear()


@pytest.fixture
def token_headers(client):
    """Fixture untuk mendapatkan JWT Token (Simulasi Login)."""
    # 1. Buat user dummy dulu
    client.post(
        "/api/v1/users/",
        json={
            "name": "tester",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    # 2. Login
    login_res = client.post(
        "/api/v1/auth/login", data={"username": "test@example.com", "password": "password123"}
    )
    token = login_res.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
