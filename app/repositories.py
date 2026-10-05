from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Car, Rental


def get_car(
    db: Session,
    car_id: int,
) -> Car | None:
    return db.get(Car, car_id)


def list_cars(
    db: Session,
    status: str | None = None,
) -> list[Car]:
    statement = select(Car)

    if status:
        statement = statement.where(
            Car.status == status
        )

    return list(db.scalars(statement).all())


def create_car(
    db: Session,
    model: str,
    year: int,
) -> Car:
    car = Car(
        model=model,
        year=year,
        status="available",
    )

    db.add(car)
    db.flush()

    return car


def get_rental(
    db: Session,
    rental_id: int,
) -> Rental | None:
    return db.get(Rental, rental_id)


def create_rental(
    db: Session,
    car_id: int,
    customer_name: str,
    start_date: datetime,
) -> Rental:
    rental = Rental(
        car_id=car_id,
        customer_name=customer_name,
        start_date=start_date,
    )

    db.add(rental)
    db.flush()

    return rental