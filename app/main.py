from fastapi import FastAPI

from .api import router
from .db import Base, engine
from . import models
import logging

from .logging_config import configure_logging

import time

from prometheus_client import generate_latest
from fastapi.responses import Response

from .metrics import (
    REQUEST_COUNT,
    REQUEST_TIME,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DriveNow Vehicle Management System",
)

configure_logging()

logger = logging.getLogger(__name__)

app.include_router(router)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    REQUEST_COUNT.inc()
    REQUEST_TIME.observe(duration)

    return response

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )

@app.get("/health")
def health():
    logger.info("Health check")
    return {"status": "ok"}