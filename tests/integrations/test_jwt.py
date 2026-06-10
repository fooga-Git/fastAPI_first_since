def test_protected_endpoint_without_token(client):
    """Доступ к защищённому эндпоинту без токена"""
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_protected_endpoint_with_valid_token(client, user_token):
    """Доступ к защищённому эндпоинту с токеном"""
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert "login" in response.json()


def test_refresh_token(client):
    """Проверка обновления токена"""
    # Регистрация
    client.post("/auth/register", data={
        "login": "refreshuser",
        "password": "123",
        "full_name": "Refresh User",
        "email": "refresh@example.com"
    })

    resp = client.post("/auth/login", data={
        "login": "refreshuser",
        "password": "123"
    })
    refresh_token = resp.json()["refresh_token"]

    resp = client.post("/auth/refresh", data={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
