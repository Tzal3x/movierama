from typing import Annotated
from fastapi import APIRouter, status, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from app.models import Movies, Users
from app.security import authorize_user
from app.database import get_db
from sqlalchemy import exc
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory='templates')
router = APIRouter(
    tags=["movies"],
    responses={404: {"description": "Not found"}}
)


@router.get("/movie_form", status_code=status.HTTP_200_OK)
def add_movie_form(request: Request):
    return templates.TemplateResponse('movie_form.html', 
                                      {"request": request})


@router.post("/movies", status_code=status.HTTP_201_CREATED)
def add_movie_form(title: Annotated[str, Form()], 
                   description:  Annotated[str, Form()],
                   user: Annotated[Users, Depends(authorize_user)],
                   db: Session = Depends(get_db)):
    if not user:
        return {'Sorry but you need to be logged in to add new movies.'}
    movie = Movies(
        title=title,
        description=description,
        user_id = user.id
    )
    try:
        db.add(movie)
        db.commit()
        db.refresh(movie)
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This movie title already exists in Movierama. "
            "Are you sure this is not a repost? 🤔"
            )
    return {
        f"Movie '{title}' has now been added!"
        }  # TODO: possible redirect
