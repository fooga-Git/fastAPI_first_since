from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_booking(client, user_token, admin_token):
    room = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"name": "Booking Room",
                "capacity": 10, "room_type": "coworking"}
    ).json()

    response = client.post(
        "/bookings",
        headers={"Authorization": f"Bearer {user_token}"},
        params={"room_id": room["id"], "slot_number": 1, "date": "2026-06-15"}
    )

    assert response.status_code == 200


def test_cancel_booking(client, user_token, admin_token):
    room = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"name": "Cancel Room",
                "capacity": 10, "room_type": "coworking"}
    ).json()

    booking = client.post(
        "/bookings",
        headers={"Authorization": f"Bearer {user_token}"},
        params={"room_id": room["id"], "slot_number": 1, "date": "2026-06-15"}
    ).json()

    response = client.delete(
        f"/bookings/{booking['id']}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200


def test_employee_cannot_cancel_others_booking(client, user_token, admin_token):
    client.post("/auth/register", data={
        "login": "user2",
        "password": "123",
        "full_name": "User Two",
        "email": "user2@example.com"
    })
    resp = client.post("/auth/login", data={
        "login": "user2",
        "password": "123"
    })
    user2_token = resp.json()["access_token"]

    room = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"name": "Test Room", "capacity": 10, "room_type": "coworking"}
    ).json()

    booking = client.post(
        "/bookings",
        headers={"Authorization": f"Bearer {user_token}"},
        params={"room_id": room["id"], "slot_number": 1, "date": "2026-06-15"}
    ).json()

    response = client.delete(
        f"/bookings/{booking['id']}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert response.status_code == 403
