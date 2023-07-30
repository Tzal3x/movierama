from typing import Annotated, Literal
from fastapi import APIRouter, status, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.models import Movies, Users, Opinions
from app.security import authorize_user
from app.database import get_db
from sqlalchemy import exc
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory='templates')
router = APIRouter(
    tags=["movies"],
    responses={404: {"description": "Not found"}}
)


@router.get("/new_movie", status_code=status.HTTP_200_OK)
def add_movie_form(request: Request):
    return templates.TemplateResponse('new_movie_form.html', 
                                      {"request": request})


@router.post("/movies", status_code=status.HTTP_201_CREATED)
def add_movie(title: Annotated[str, Form()], 
             description:  Annotated[str, Form()],
             request: Request,
             user: Annotated[Users, Depends(authorize_user)],
             db: Session = Depends(get_db)):
    if not user:
        return templates.TemplateResponse(
            'error_go_back.html', 
            {"request": request,
            "error_message": "You are not logged in!",
            "error_details": 'Sorry but you need to be logged in to add new movies.',
            "go_back_url": "'/new_movie'"
            }, status_code=status.HTTP_401_UNAUTHORIZED)
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
        return templates.TemplateResponse(
            'error_go_back.html', 
            {"request": request,
            "error_message": "Movie title already exists!",
            "error_details": "Are you sure this is not a repost? 🤔",
            "go_back_url": "'/new_movie'"
            }, status_code=status.HTTP_409_CONFLICT)
        
    response_template = templates.TemplateResponse('new_movie_success.html', 
                                      {"request": request,
                                       "title": title,
                                       "success": f"Movie '{title}' has now been added!",
                                       "movie_id": f"{movie.id}"},
                                       status_code=status.HTTP_201_CREATED)
    return response_template


@router.get("/movies", response_class=HTMLResponse)
def get_movies(loggedin_user: Annotated[Users, Depends(authorize_user)],
               request: Request,
               user_id: int = None,
               offset: int = 0,  # used for pagination
               sort_by: Literal['date', 'likes', 'hates'] = "date",
               db: Session = Depends(get_db)):
    """
    This is the endpoint used as the homepage. 
    """
    OFFSET_STEP = 5
    query = db.query(Movies)\
                     .filter(Movies.user_id == user_id 
                             if user_id else True)
    if sort_by == 'date':
        query = query.order_by(Movies.date.desc())
    elif sort_by == 'likes':
        query = query.order_by(Movies.likes.desc())
    elif sort_by == 'hates':
        query = query.order_by(Movies.hates.desc())
    movies = query.offset(offset).limit(5).all()
    
    processed_movies = add_template_fields(movies, loggedin_user, db)
    if len(movies) < OFFSET_STEP:
        next_button_url = None
    else:
        current_url = f"/movies?sort_by=date"
        current_url += f"&user_id={user_id}" if user_id else ""
        next_button_url = current_url + f"&offset={offset + OFFSET_STEP}"

    return templates.TemplateResponse('homepage.html', 
                                      {"request": request,
                                       "user_id": user_id,
                                       "logged_in_usr": loggedin_user,
                                       "processed_movies": processed_movies,
                                       "next_button_url": next_button_url,
                                       })


def add_template_fields(movies: list[Movies], 
                        loggedin_user: Users | None, 
                        db: Session) -> list[dict]:
    """
    Adds additional fields to each movie in order 
    to extract them in the Jinja2 homepate.html template.
    Such fields include the user relationship with the movie.
    
    i.e. Was it posted by him? Has he voted for it? etc
    """
    result = []
    for movie in movies:
        movie_dict = movie.__dict__
        username = movie.user.username
        movie_dict["user_url"] = f"/movies/?user_id={movie.user_id}"
        movie_dict["username"] = username
        if loggedin_user:
            has_created = db.query(Movies)\
                            .filter(Movies.user_id == loggedin_user.id,
                                     Movies.id == movie.id)\
                            .first()
            if has_created:
                movie_dict["you_posted_this"] = True
            else:
                movie_dict["you_posted_this"] = False

            has_voted = db.query(Opinions)\
                          .filter(Opinions.user_id == loggedin_user.id,
                                  Opinions.movie_id == movie.id)\
                          .first()          
            movie_dict["has_voted"] = bool(has_voted) 
            if has_voted:
                movie_dict["liked_or_hated"] = has_voted.opinion
                movie_dict["unvote_url"] = f"/opinions/undo?movie_id={movie.id}"

        result.append(movie_dict)
    return result
