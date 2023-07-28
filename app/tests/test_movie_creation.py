from app.tests.conftest import client
from fastapi import status
from app.tests.cases.movie_cases import test_movies


def test_create_new_movie_valid(loggedin_user):
    movie = test_movies[0]
    response = client.post('/movies', 
                           data=movie,
                           cookies=loggedin_user['cookie'])
    assert response.status_code == status.HTTP_201_CREATED


def test_create_new_movie_existing_title(loggedin_user):
    movie = {
        "title": "Back to the Future",
        "description": "A classic time-travel adventure"
        }
    client.post('/movies', data=movie, cookies=loggedin_user['cookie'])
    response = client.post('/movies', 
                           data=movie,
                           cookies=loggedin_user['cookie'])
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_new_movie_missing_title(loggedin_user):
    movie = {
        "description": "A classic time-travel adventure"
        }
    response = client.post('/movies', 
                           data=movie,
                           cookies=loggedin_user['cookie'])
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_new_movie_missing_description(loggedin_user):
    movie = {
        "title": "Back to the Future"
        }
    response = client.post('/movies', 
                           data=movie,
                           cookies=loggedin_user['cookie'])
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
