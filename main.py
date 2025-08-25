from fastapi import FastAPI

from .backend.database import get_engine, Base
from .backend.logic import (
    user_routes, chat_routes,
)
from .tests import app

app = FastAPI(
    title="Messenger API",
    version="v0.0",
)

@app.on_event("startup")
def startup():
    print("start test")
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=get_engine())

app.include_router(user_routes.router)
app.include_router(chat_routes.router)