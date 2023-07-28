from contextlib import contextmanager
from app.tests.conftest import client
from fastapi import status
from app.database import SessionLocal
from app.models import Users
from app.tests.cases.user_cases import test_users


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def teardown(username: str):
    """
    Delete a user after the test was run.
    """
    with get_db() as db:
        db.query(Users).filter(Users.username == username).delete()
        db.commit()


def test_register_user_valid():
    """
    A user providing a username and password should
    be registered successfully. 
    """
    user = test_users[0]
    response = client.post('/users', data=user)
    assert response.status_code == status.HTTP_201_CREATED
    teardown(username = user["username"])


def test_register_existing_user():
    """
    Create a user, and then try to create the same user again.
    This is expected to fail obviously due to the unique 
    username constraint.
    """
    user = test_users[0]
    client.post('/users', data=user)
    response = client.post('/users', data=user)
    assert response.status_code == status.HTTP_409_CONFLICT
    teardown(username = user["username"])


def test_register_user_missing_username():
    """
    Try creating a user without a username.
    """
    user =  {
    "password": "pop!pop!pop!",
    }
    response = client.post('/users', data=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_user_missing_password():
    """
    Try creating a user without a password.
    """
    user =  {
    "username": "PopCornLover",
    }
    response = client.post('/users', data=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_user_empty_username():
    """
    Try creating a user with empty a username.
    """
    user = {
    "username": "",
    "password": "NarniaMatrix*18"
    }
    response = client.post('/users', data=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
