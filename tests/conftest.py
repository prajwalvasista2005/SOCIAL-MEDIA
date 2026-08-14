import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models,utils
from app.config import settings
from urllib.parse import quote_plus

password = quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
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
def test_post(session, test_user):
    post = models.Post(
        title="Test Title",
        content="Test Content",
        owner_id=test_user.id
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post

@pytest.fixture
def test_posts(session, test_user):
    posts_data = [
        {
            "title": "First Post",
            "content": "Content 1",
            "owner_id": test_user.id
        },
        {
            "title": "Second Post",
            "content": "Content 2",
            "owner_id": test_user.id
        }
    ]

    posts = [models.Post(**post) for post in posts_data]

    session.add_all(posts)
    session.commit()

    return posts

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

@pytest.fixture
def test_comment(
    session,
    test_post,
    test_user
):
    comment = models.Comment(
        content="Test Comment",
        post_id=test_post.id,
        user_id=test_user.id
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment

