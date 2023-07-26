from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import (APIRouter, status, Request,
                     HTTPException, Depends, Form, Response)
from sqlalchemy.orm import Session
from app.security import authenticate_user, create_access_token
from app.database import get_db
from app.schemas import Token
from fastapi.templating import Jinja2Templates
from os import environ


templates = Jinja2Templates(directory='templates')
router = APIRouter(
    tags=["authentication"],
    responses={404: {"description": "Not found"}}
)


@router.get("/login", 
             response_class=HTMLResponse,
             status_code=status.HTTP_201_CREATED)
async def login_form(request: Request):
    return templates.TemplateResponse('login.html', 
                                      {"request": request})


@router.post("/set_auth_cookie", 
             status_code=status.HTTP_201_CREATED)
def login(username: Annotated[str, Form()], 
          password:  Annotated[str, Form()],
          response: Response,
          request: Request,
          db: Session = Depends(get_db)):
    """
    Creates a token and saves it in a cookie inside the browser. 
    """
    user = authenticate_user(db, username, password)
    if _authentication_failed := not user:
        raise HTTPException(status_code=400, 
                            detail="Incorrect username or password")
    token = Token(access_token=create_access_token(data={'sub': user.username}))
    # On "expires" cookie param bellow I convert the seconds to minutes since
    #  the expires == how many seconds after should it expire.
    response.set_cookie(key="token", 
                        value=token.access_token,
                        expires=int(environ["ACCESS_TOKEN_EXPIRE_MINUTES"])*60)
    return {"You have successfully logged in!"}


@router.delete("/logout", status_code=status.HTTP_205_RESET_CONTENT)
def logout(response: Response):
    response.delete_cookie("token")
    return {"Successfully logged out"}
