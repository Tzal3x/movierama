from fastapi import FastAPI
from app.routers import (
    registration,
    users
)


app = FastAPI()
app.include_router(registration.router)
app.include_router(users.router)


@app.get('/')
def root() -> dict:
    """Root path"""
    # TODO if user logged in return logged in homepage
    # TODO if user not logged in show not logged in homepage
    return {"message": "Welcome to MOVIERAMA! "
            "Go to '/docs' for the API documentation."}
