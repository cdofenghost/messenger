from fastapi import FastAPI

from .backend.database import get_engine, Base
from .backend.logic.routes import (
    chats, users,
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

app.include_router(users.router)
app.include_router(chats.router)