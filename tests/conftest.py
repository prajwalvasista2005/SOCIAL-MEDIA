import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models,utils


SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:"
    "prajwal%40123@"
    "127.0.0.1:5432/"
    "fastapi_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def session():
    print("CREATING TEST DATABASE TABLES")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    print("USING TEST DB")

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def test_user(session):
    user = models.User(
        email="test@gmail.com",
        username="testuser",
        password=utils.hash("password123")
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@pytest.fixture
def token(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    return response.json()["access_token"]

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client