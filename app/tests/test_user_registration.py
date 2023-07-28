from app.tests.conftest import client, teardown_user, user
from fastapi import status
from app.tests.cases.user_cases import test_users


def test_register_user_valid():
    """
    A user providing a username and password should
    be registered successfully. 
    """
    user = test_users[0]
    response = client.post('/users', data=user)
    assert response.status_code == status.HTTP_201_CREATED
    teardown_user(username=user["username"])


def test_register_existing_user(user):
    """
    Create a user, and then try to create the same user again.
    This is expected to fail obviously due to the unique 
    username constraint.
    """
    client.post('/users', data=user)
    response = client.post('/users', data=user)
    assert response.status_code == status.HTTP_409_CONFLICT


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
