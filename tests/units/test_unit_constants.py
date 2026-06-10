from app.core.constants import DAY_SLOTS, NIGHT_SLOTS


def test_day_slots_count():
    assert len(DAY_SLOTS) == 6


def test_night_slots_count():
    assert len(NIGHT_SLOTS) == 3


def test_day_slots_structure():
    for slot in DAY_SLOTS:
        assert "number" in slot
        assert "time_range" in slot
        assert "is_night" in slot
        assert slot["is_night"] is False


def test_night_slots_structure():
    for slot in NIGHT_SLOTS:
        assert "number" in slot
        assert "time_range" in slot
        assert "is_night" in slot
        assert slot["is_night"] is True


def test_day_slots_numbers():
    numbers = [slot["number"] for slot in DAY_SLOTS]
    assert numbers == [1, 2, 3, 4, 5, 6]


def test_night_slots_numbers():
    numbers = [slot["number"] for slot in NIGHT_SLOTS]
    assert numbers == [7, 8, 9]
