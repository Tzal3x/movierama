from app.tests.conftest import (
    client, 
    loggedin_user, 
    loggedin_user_2
    )
from fastapi import status
from app.tests.cases.movie_cases import test_movies
import json


def test_vote_a_movie(loggedin_user, loggedin_user_2):
    """
    Just vote for a movie
    """
    movie = test_movies[0]
    # User 1 adds movie.
    add_movie_response = client.post('/movies', 
                                    data=movie, 
                                    cookies=loggedin_user['cookie'])
    movie_id = json.loads(add_movie_response.content)['movie_id']
    # User 2 votes it.
    vote_response =  client.post(
        f'/opinions/?movie_id={movie_id}&opinion=1', # 1 == like
        cookies=loggedin_user_2['cookie']
        )
    assert vote_response.status_code == status.HTTP_201_CREATED


def test_cant_vote_your_own(loggedin_user):
    """
    If you are the one that posted this movie, 
    you shouldn't be able to vote for it.
    """
    movie = test_movies[0]
    # User 1 adds movie.
    add_movie_response = client.post('/movies', 
                                    data=movie, 
                                    cookies=loggedin_user['cookie'])
    movie_id = json.loads(add_movie_response.content)['movie_id']
    # User 1 tries to vote for it.
    vote_response =  client.post(
        f'/opinions/?movie_id={movie_id}&opinion=1', # 1 == like
        cookies=loggedin_user['cookie']
        )
    assert vote_response.status_code == status.HTTP_409_CONFLICT


def test_cant_multiple_vote(loggedin_user, loggedin_user_2):
    """
    If you have already liked or hated a movie, 
    you shouldn't be able to vote again on the same
    movie before unvoting it first. 
    """
    movie = test_movies[0]
    # User 1 adds movie.
    add_movie_response = client.post('/movies', 
                                    data=movie, 
                                    cookies=loggedin_user['cookie'])
    movie_id = json.loads(add_movie_response.content)['movie_id']
    # User 2 votes it.
    client.post(
            f'/opinions/?movie_id={movie_id}&opinion=1', # 1 == like
            cookies=loggedin_user_2['cookie']
        )
    # User 2 tried to vote again.
    vote_2_response =  client.post(
        f'/opinions/?movie_id={movie_id}&opinion=2', # 2 == hate
        cookies=loggedin_user_2['cookie']
        )
    assert vote_2_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
