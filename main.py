from fastapi import FastAPI
from .backend.database import get_engine, Base

app = FastAPI(
    title="Messenger API",
    version="v0.0",
)

@app.on_event("startup")
def startup():
    print("start test")
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=get_engine())