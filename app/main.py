from fastapi import FastAPI

from .api import router
from .db import Base, engine
from . import models


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DriveNow Vehicle Management System",
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}