from typing import Annotated
from fastapi import APIRouter, status, Request, Depends, Form, HTTPException
from app.models import Opinions, Users
from app.security import authorize_user
from app.database import get_db
from sqlalchemy import exc
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/opinions",
    tags=["opinions"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    movie_id: int,
    opinion: bool,
    user: Annotated[Users, Depends(authorize_user)],
    db: Session = Depends(get_db)):
    if not user:
        return {'Sorry but you need to be logged in to vote for a movie.'}
    opinion = Opinions(
        movie_id=movie_id,
        user_id=user.id,
        opinion=opinion,
    )
    
    try:
        db.add(opinion)
        db.commit()
        db.refresh(opinion)
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="🙅‍♂️ Error: Have you already voted this movie? "
            "Remember that you can't vote for a movie you have posted."
            )


@router.delete("/unvote", status_code=status.HTTP_204_NO_CONTENT)
def unvote( 
    movie_id: int,
    user: Annotated[Users, Depends(authorize_user)],
    db: Session = Depends(get_db)):
    """
    Unlike or unhate a movie.

    Tip: You have to unvote first, in order to change
    your vote. This happens because a user can only
    vote once for a movie.
    """
    try:
        db.query(Opinions)\
          .filter(user.id == Opinions.user_id, 
                  movie_id == Opinions.movie_id)\
          .delete()
        db.commit()
    except exc.SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Could not delete user.")
