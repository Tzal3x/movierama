import pytest
from fastapi.testclient import TestClient
from contextlib import contextmanager
from app.database import SessionLocal
from ..main import app
from app.models import Users, Movies
from app.tests.cases.user_cases import test_users
from app.security import create_access_token

client = TestClient(app)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def teardown_user(username: str):
    """
    Delete a user after the test was run.
    We can deleting by username due to the unique constraint.  
    """
    with get_db() as db:
        db.query(Users).filter(Users.username == username).delete()
        db.commit()


def teardown_movie(title: str):
    """
    Delete a movie after the test was run.
    We can deleting by title due to the unique constraint.  
    """
    with get_db() as db:
        db.query(Movies).filter(Movies.title == title).delete()
        db.commit()


@pytest.fixture
def user():
    """
    Create a simple user. 

    This user has no movies added, and has
    not voted the movies of others. 
    """
    user = test_users[0]
    client.post('/users', data=user)
    yield user
    teardown_user(user["username"])


@pytest.fixture
def loggedin_user(user):
    token = create_access_token(data={"sub": user["username"]})
    user["cookie"] = [("token", token)]
    yield user
