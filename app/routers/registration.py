from fastapi.responses import HTMLResponse
from fastapi import (
    APIRouter, status,
    Request
)
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')
router = APIRouter(
    prefix="/register",
    tags=["register"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", 
             response_class=HTMLResponse,
             status_code=status.HTTP_201_CREATED)
async def register_form(request: Request):
    return templates.TemplateResponse('register.html', 
                                      {"request": request})
