from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from . import repositories, services
from .db import get_db
from .schemas import (
    CarCreate,
    CarResponse,
    CarStatus,
    CarUpdate,
    RentalCreate,
    RentalResponse,
)


router = APIRouter()


@router.post(
    "/cars",
    response_model=CarResponse,
    status_code=201,
)
def create_car(
    data: CarCreate,
    db: Session = Depends(get_db),
):
    return services.add_car(
        db,
        data.model,
        data.year,
    )


@router.get(
    "/cars",
    response_model=list[CarResponse],
)
def list_cars(
    status: CarStatus | None = None,
    db: Session = Depends(get_db),
):
    return repositories.list_cars(
        db,
        status,
    )


@router.get(
    "/cars/{car_id}",
    response_model=CarResponse,
)
def get_car(
    car_id: int,
    db: Session = Depends(get_db),
):
    car = repositories.get_car(
        db,
        car_id,
    )

    if car is None:
        return Response(
            content="Car not found",
            status_code=404,
        )

    return car


@router.patch(
    "/cars/{car_id}",
    response_model=CarResponse,
)
def update_car(
    car_id: int,
    data: CarUpdate,
    db: Session = Depends(get_db),
):
    return services.update_car(
        db,
        car_id,
        data.model,
        data.year,
        data.status,
    )


@router.delete(
    "/cars/{car_id}",
    status_code=204,
)
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
):
    services.delete_car(db, car_id)
    return Response(status_code=204)


@router.post(
    "/rentals",
    response_model=RentalResponse,
    status_code=201,
)
def create_rental(
    data: RentalCreate,
    db: Session = Depends(get_db),
):
    return services.register_rental(
        db,
        data.car_id,
        data.customer_name,
        data.start_date,
    )


@router.post(
    "/rentals/{rental_id}/end",
    response_model=RentalResponse,
)
def finish_rental(
    rental_id: int,
    db: Session = Depends(get_db),
):
    return services.end_rental(
        db,
        rental_id,
    )