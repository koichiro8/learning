import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .apiv1.todo import todo_router
from .database import get_enigne, initialize_session
from .errors import NotFoundError, TitleLengthError, TodoError


async def index():
    return "Hello, world!"


async def todo_exception_handler(request: Request, exc: TodoError):
    status_code = 500
    if isinstance(exc, TitleLengthError):
        status_code = 400
    elif isinstance(exc, NotFoundError):
        status_code = 404
    return JSONResponse(status_code=status_code, content={"code": exc.code, "detail": str(exc)})


def create_app():
    app = FastAPI()
    app.add_api_route("/", index)
    app.include_router(todo_router)
    app.add_exception_handler(TodoError, todo_exception_handler)
    initialize_session(get_enigne(os.environ["DB_URL"]))
    return app
