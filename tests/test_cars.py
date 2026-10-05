from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_car():
    response = client.post(
        "/cars",
        json={
            "model": "Toyota Corolla",
            "year": 2024,
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "available"


def test_list_cars():
    response = client.get("/cars")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_car():
    create_response = client.post(
        "/cars",
        json={
            "model": "Honda Civic",
            "year": 2023,
        },
    )

    car_id = create_response.json()["id"]

    response = client.patch(
        f"/cars/{car_id}",
        json={
            "status": "maintenance",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "maintenance"