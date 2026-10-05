from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import repositories


def add_car(
    db: Session,
    model: str,
    year: int,
):
    car = repositories.create_car(
        db,
        model,
        year,
    )

    db.commit()
    db.refresh(car)

    return car


def update_car(
    db: Session,
    car_id: int,
    model: str | None,
    year: int | None,
    status: str | None,
):
    car = repositories.get_car(db, car_id)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found",
        )

    if model is not None:
        car.model = model

    if year is not None:
        car.year = year

    if status is not None:
        car.status = status

    db.commit()
    db.refresh(car)

    return car


def delete_car(
    db: Session,
    car_id: int,
):
    car = repositories.get_car(db, car_id)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found",
        )

    if car.rentals:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete car with rental history",
        )

    db.delete(car)
    db.commit()


def register_rental(
    db: Session,
    car_id: int,
    customer_name: str,
    start_date: datetime,
):
    car = repositories.get_car(db, car_id)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found",
        )

    if car.status != "available":
        raise HTTPException(
            status_code=409,
            detail="Car is not available",
        )

    rental = repositories.create_rental(
        db,
        car_id,
        customer_name,
        start_date,
    )

    car.status = "in_use"

    db.commit()
    db.refresh(rental)

    return rental


def end_rental(
    db: Session,
    rental_id: int,
):
    rental = repositories.get_rental(
        db,
        rental_id,
    )

    if rental is None:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    if rental.end_date is not None:
        raise HTTPException(
            status_code=409,
            detail="Rental already ended",
        )

    rental.end_date = datetime.utcnow()

    car = repositories.get_car(
        db,
        rental.car_id,
    )

    if car is not None:
        car.status = "available"

    db.commit()
    db.refresh(rental)

    return rental