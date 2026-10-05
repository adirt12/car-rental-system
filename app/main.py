import logging
import time

from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest
from sqlalchemy import func

from . import models
from .api import router
from .db import Base, SessionLocal, engine
from .logging_config import configure_logging
from .metrics import (
    ACTIVE_CARS,
    ONGOING_RENTALS,
    REQUEST_COUNT,
    REQUEST_TIME,
)
from .models import Car, Rental


Base.metadata.create_all(bind=engine)

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="DriveNow Vehicle Management System",
)

app.include_router(router)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    REQUEST_COUNT.inc()
    REQUEST_TIME.observe(duration)

    return response


def update_metrics():
    db = SessionLocal()

    try:
        active_cars = (
            db.query(Car)
            .filter(Car.status != "maintenance")
            .count()
        )

        ongoing_rentals = (
            db.query(Rental)
            .filter(Rental.end_date.is_(None))
            .count()
        )

        ACTIVE_CARS.set(active_cars)
        ONGOING_RENTALS.set(ongoing_rentals)
    finally:
        db.close()


@app.get("/health")
def health():
    logger.info("Health check")
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    update_metrics()

    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )