from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


CarStatus = Literal[
    "available",
    "in_use",
    "maintenance",
]


class CarCreate(BaseModel):
    model: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1886, le=2100)


class CarUpdate(BaseModel):
    model: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    year: int | None = Field(
        default=None,
        ge=1886,
        le=2100,
    )
    status: CarStatus | None = None


class CarResponse(BaseModel):
    id: int
    model: str
    year: int
    status: CarStatus

    model_config = {
        "from_attributes": True
    }


class RentalCreate(BaseModel):
    car_id: int
    customer_name: str = Field(
        min_length=1,
        max_length=100,
    )
    start_date: datetime


class RentalResponse(BaseModel):
    id: int
    car_id: int
    customer_name: str
    start_date: datetime
    end_date: datetime | None

    model_config = {
        "from_attributes": True
    }