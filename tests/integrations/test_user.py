from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_set_role(client, admin_token):
    resp_reg = client.post("/auth/register", data={
        "login": "touser",
        "password": "123",
        "full_name": "To User",
        "email": "touser@example.com"
    })
    user_id = resp_reg.json()["user_id"]

    response = client.post(
        "/admin/set-role",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"user_id": user_id, "role": "admin"}
    )

    assert response.status_code == 200


def test_delete_user(client, admin_token):  # <- добавить client
    resp_reg = client.post("/auth/register", data={
        "login": "deluser",
        "password": "123",
        "full_name": "Delete User",
        "email": "del@example.com"
    })
    user_id = resp_reg.json()["user_id"]

    response = client.delete(
        f"/admin/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
