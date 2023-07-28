from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import APIRouter, status, Form, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from app.database import get_db
from app.security import get_password_hash
from app.models import Users
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory='templates')
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", 
             status_code=status.HTTP_201_CREATED,
             response_class=HTMLResponse)
def register_user(
    request: Request,
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
    return templates.TemplateResponse('registration_success.html', 
                                      {"request": request})
