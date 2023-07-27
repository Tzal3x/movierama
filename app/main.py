from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from app.routers import (
    registration,
    authentication,
    users,
    movies,
    opinions
)


app = FastAPI()
app.include_router(registration.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(movies.router)
app.include_router(opinions.router)


@app.get('/')
def root():
    return RedirectResponse(
        '/movies', 
        status_code=status.HTTP_302_FOUND)