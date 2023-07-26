from typing import Annotated
from fastapi import FastAPI, Depends
from app.routers import (
    registration,
    authentication,
    users
)
from app.security import authorize_user


app = FastAPI()
app.include_router(registration.router)
app.include_router(users.router)
app.include_router(authentication.router)


@app.get('/')
def root(user: Annotated[bool, Depends(authorize_user)]):
    """Root path"""
    if user:
        # TODO - go to homepage
        return {f"message": f"Welcome to MovieRama {user.username}! "
            "Go to '/docs' for the API documentation."}
    else:
        # TODO - go to homepage of not logged in
        return {"You are not logged in!"}
    