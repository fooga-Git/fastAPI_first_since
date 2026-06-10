from datetime import date

from app.schemas.user import UserResponse, SetRoleRequest
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.schemas.slot import SlotResponse
from app.schemas.booking import BookingCreate
from app.schemas.token import Token


def test_user_response_schema():
    user = UserResponse(
        id=1,
        login="testuser",
        full_name="Test User",
        email="test@example.com",
        role="employee"
    )
    assert user.id == 1
    assert user.login == "testuser"
    assert user.full_name == "Test User"
    assert user.email == "test@example.com"
    assert user.role == "employee"


def test_set_role_request_schema():
    req = SetRoleRequest(user_id=5, role="admin")
    assert req.user_id == 5
    assert req.role == "admin"


def test_room_create_schema():
    room = RoomCreate(name="Conference", capacity=20, room_type="coworking")
    assert room.name == "Conference"
    assert room.capacity == 20
    assert room.room_type == "coworking"


def test_room_update_schema():
    room = RoomUpdate(capacity=30, room_type="podcast")
    assert room.capacity == 30
    assert room.room_type == "podcast"


def test_room_response_schema():
    room = RoomResponse(id=1, name="Meeting", capacity=10,
                        room_type="coworking")
    assert room.id == 1
    assert room.name == "Meeting"
    assert room.capacity == 10
    assert room.room_type == "coworking"


def test_slot_response_schema():
    slot = SlotResponse(number=1, room_id=2,
                        time_range="09:00-11:00", is_night=False)
    assert slot.number == 1
    assert slot.room_id == 2
    assert slot.time_range == "09:00-11:00"
    assert slot.is_night is False


def test_booking_create_schema():
    booking = BookingCreate(room_id=1, slot_number="3", date=date(2026, 6, 15))
    assert booking.room_id == 1
    assert booking.slot_number == "3"
    assert booking.date == date(2026, 6, 15)


def test_token_schema():
    token = Token(access_token="abc123",
                  refresh_token="def456", token_type="bearer")
    assert token.access_token == "abc123"
    assert token.refresh_token == "def456"
    assert token.token_type == "bearer"
