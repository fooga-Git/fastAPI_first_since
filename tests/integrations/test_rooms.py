from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)


def test_create_room(client, admin_token):

    coworking_name = f"Coworking Room {int(time.time())}"
    coworking_response = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"name": coworking_name,
                "capacity": 10, "room_type": "coworking"}
    )
    assert coworking_response.status_code == 200
    coworking_id = coworking_response.json()["id"]
    slots_response = client.get(
        f"/rooms/{coworking_id}/slots",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    coworking_slots = slots_response.json()
    for slot in coworking_slots:
        assert not slot["is_night"], "В коворкинге только дневные слоты"
    podcast_name = f"Podcast Room {int(time.time())}"
    podcast_response = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"name": podcast_name, "capacity": 5, "room_type": "podcast"}
    )
    assert podcast_response.status_code == 200
    podcast_id = podcast_response.json()["id"]
    slots_response = client.get(
        f"/rooms/{podcast_id}/slots",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    podcast_slots = slots_response.json()
    has_night = any(slot["is_night"] for slot in podcast_slots)
    assert has_night, "В подкасте должны быть ночные слоты"


def test_create_room_unauthorized(user_token):
    response = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {user_token}"},
        params={"name": "Unauthorized Room",
                "capacity": 5, "room_type": "coworking"}
    )
    assert response.status_code == 403


def test_get_rooms(client, user_token):
    response = client.get(
        "/rooms",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_room(client, admin_token):
    room = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"name": "Update Room", "capacity": 5, "room_type": "coworking"}
    ).json()

    response = client.patch(
        f"/rooms/{room['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"capacity": 20}
    )
    assert response.status_code == 200
    assert response.json()["capacity"] == 20


def test_delete_room(client, admin_token):
    room = client.post(
        "/rooms",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"name": "Delete Room", "capacity": 3, "room_type": "coworking"}
    ).json()

    response = client.delete(
        f"/rooms/{room['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
