import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# --- ride_cost tests ---
def test_ride_cost_invalid_bike_type():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("tandem", 30, False, False)


def test_ride_cost_invalid_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)


def test_ride_cost_subscriber_free_first_block():
    assert ride_cost("standard", 25, True, False) == 0


def test_ride_cost_standard_peak():
    assert ride_cost("standard", 45, False, True) == 55


def test_ride_cost_long_ride_surcharge():
    assert ride_cost("electric", 200, True, False) == 310


# --- dock_status tests ---
def test_dock_status_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)


def test_dock_status_invalid_bike_count():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(12, 10)


def test_dock_status_empty():
    assert dock_status(0, 10) == "empty"


def test_dock_status_full():
    assert dock_status(10, 10) == "full"


def test_dock_status_few_bikes():
    assert dock_status(2, 10) == "few bikes"


def test_dock_status_few_slots():
    assert dock_status(8, 10) == "few slots"


def test_dock_status_available():
    assert dock_status(5, 10) == "available"


# --- can_unlock tests ---
def test_can_unlock_active_ride():
    assert can_unlock(200, True, 25) is False


def test_can_unlock_underage():
    assert can_unlock(200, False, 15) is False


def test_can_unlock_teen():
    assert can_unlock(100, False, 16) is True


def test_can_unlock_adult():
    assert can_unlock(50, False, 20) is True