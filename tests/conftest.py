import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture
def session():
    """
    Fixture that creates a new in-memory SQLite
    database for each test case.
    """

    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    """
    This fixture sets up a TestClient for the FastAPI application, overriding
    the default dependency for database sessions with a fake dependency.

    By overriding the `get_session` dependency, it ensures that the application
    uses an in-memory SQLite database during tests, instead of the production
    database.

    Returns:
        TestClient: A test client instance configured with the overridden
        dependencies.
    """  # noqa: W293

    def fake_session():
        return session

    with TestClient(app) as client:
        client.app.dependency_overrides[get_session] = fake_session

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    """
    Fixture that creates a new user in the in-memory database.
    """

    pwd = 'test'
    user = User(
        username='Test',
        email='test@test.com',
        password=get_password_hash(pwd),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
