from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import APIRouter, status, Form, Depends
from fastapi.exceptions import HTTPException
from app.database import get_db
from app.security import get_password_hash
from app.models import Users


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(
    username: Annotated[str, Form()], 
    password:  Annotated[str, Form()],
    db: Session = Depends(get_db),
    ):
    hashed_password = get_password_hash(password)
    db_user = Users(username=username, password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration failed: Username already exists.")
    return {
        "You have successfully registered! 🎉 "\
        "You can now log in to Movierama. Enjoy!"
        }  # TODO: I could directly send them the login form
    

@router.get("/", status_code=status.HTTP_200_OK)
def get_movies_of_a_user(username, sort_by):
    pass  # TODO

