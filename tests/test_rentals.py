from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_rental_changes_car_status():
    car = client.post(
        "/cars",
        json={
            "model": "Mazda 3",
            "year": 2022,
        },
    ).json()

    response = client.post(
        "/rentals",
        json={
            "car_id": car["id"],
            "customer_name": "Alice",
            "start_date": datetime.now().isoformat(),
        },
    )

    assert response.status_code == 201

    car_response = client.get(
        f"/cars/{car['id']}"
    )

    assert car_response.json()["status"] == "in_use"


def test_end_rental_makes_car_available():
    car = client.post(
        "/cars",
        json={
            "model": "Kia Rio",
            "year": 2021,
        },
    ).json()

    rental = client.post(
        "/rentals",
        json={
            "car_id": car["id"],
            "customer_name": "Bob",
            "start_date": datetime.now().isoformat(),
        },
    ).json()

    response = client.post(
        f"/rentals/{rental['id']}/end"
    )

    assert response.status_code == 200

    car_response = client.get(
        f"/cars/{car['id']}"
    )

    assert car_response.json()["status"] == "available"