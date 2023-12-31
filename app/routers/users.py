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
        return templates.TemplateResponse(
            'error_go_back.html', 
            {"request": request,
            "error_message": "🙅‍♂️ Registration failed! ",
            "error_details": 'This username is already taken.',
            "go_back_url": "'/register'"
            }, status_code=status.HTTP_409_CONFLICT)
        
    response_template = templates.TemplateResponse('registration_success.html', 
                                      {"request": request})
    response_template.status_code = status.HTTP_201_CREATED
    return response_template
