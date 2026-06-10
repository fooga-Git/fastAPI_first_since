from app.core.security import (
    create_access_token,
    decode_token,
    create_refresh_token,
)


def test_valid_jwt_token():
    """Проверка создания и декодирования JWT"""
    data = {"user_id": 1}
    token = create_access_token(data)
    decoded = decode_token(token)

    assert decoded["user_id"] == 1
    assert "exp" in decoded


def test_expired_token():
    """Проверка просроченного токена"""
    from datetime import timedelta
    data = {"user_id": 1}
    token = create_access_token(data, expires_delta=timedelta(minutes=-1))
    decoded = decode_token(token)

    assert decoded is None


def test_invalid_token():
    """Проверка невалидного токена"""
    invalid_token = "not.a.valid.token"
    decoded = decode_token(invalid_token)

    assert decoded is None


def test_token_with_custom_data():
    token = create_access_token({"user_id": 99, "custom": "value"})
    decoded = decode_token(token)
    assert decoded["user_id"] == 99
    assert decoded["custom"] == "value"


def test_refresh_token_creation():
    token = create_refresh_token({"user_id": 1})
    decoded = decode_token(token)
    assert decoded["user_id"] == 1
    assert "exp" in decoded


def test_empty_data_token():
    token = create_access_token({})
    decoded = decode_token(token)
    assert "exp" in decoded
