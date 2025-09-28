from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .backend.database import get_engine, Base
from .backend.logic.routes import (
    chats, users, messages,
)
from .tests import app

app = FastAPI(
    title="Messenger API",
    version="v0.2",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event("startup")
def startup():
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=get_engine())

app.include_router(users.router)
app.include_router(chats.router)
app.include_router(messages.router)
