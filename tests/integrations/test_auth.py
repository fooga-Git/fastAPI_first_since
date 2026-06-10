

def test_register(client):
    response = client.post("/auth/register", data={
        "login": "testuser",
        "password": "123",
        "full_name": "Test User",
        "email": "test@example.com"
    })
    assert response.status_code == 200


def test_login(user_token):
    assert user_token is not None
