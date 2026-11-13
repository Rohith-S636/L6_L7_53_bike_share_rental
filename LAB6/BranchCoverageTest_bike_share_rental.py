import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# --- ride_cost branch tests ---
@pytest.mark.parametrize(
    "bike_type, minutes, is_subscriber, is_peak, expected",
    [
        ("standard", 45, False, False, 40),      # non-subscriber, off-peak, <= 180
        ("standard", 45, False, True, 55),       # is_peak=True, bike_type != "cargo"
        ("cargo", 30, False, True, 50),          # is_peak=True, bike_type == "cargo" (short-circuit False)
        ("electric", 20, True, False, 0),        # subscriber, blocks <= 0 (True)
        ("electric", 45, True, False, 35),       # subscriber, blocks > 0 (False)
        ("standard", 180, False, False, 120),    # boundary: minutes == 180 (minutes > 180 False)
        ("standard", 181, False, False, 240),    # boundary: minutes == 181 (minutes > 180 True)
    ],
)
def test_ride_cost_valid_branches(bike_type, minutes, is_subscriber, is_peak, expected):
    assert ride_cost(bike_type, minutes, is_subscriber, is_peak) == expected


@pytest.mark.parametrize(
    "bike_type, minutes, error_msg",
    [
        ("scooter", 30, "unknown bike type"),
        ("standard", 0, "invalid duration"),
        ("standard", -10, "invalid duration"),
    ],
)
def test_ride_cost_error_branches(bike_type, minutes, error_msg):
    with pytest.raises(ValueError, match=error_msg):
        ride_cost(bike_type, minutes, False, False)


# --- dock_status branch tests ---
@pytest.mark.parametrize(
    "bikes_docked, capacity, expected",
    [
        (0, 10, "empty"),        # bikes_docked == 0 (True)
        (10, 10, "full"),        # free_slots == 0 (True)
        (1, 10, "few bikes"),    # bikes_docked <= 2 (True)
        (2, 10, "few bikes"),    # boundary: bikes_docked == 2
        (8, 10, "few slots"),    # boundary: free_slots == 2 (True)
        (9, 10, "few slots"),    # free_slots == 1 (True)
        (5, 10, "available"),    # all special conditions False
        (1, 2, "few bikes"),     # bikes_docked <= 2 evaluated before free_slots <= 2
    ],
)
def test_dock_status_valid_branches(bikes_docked, capacity, expected):
    assert dock_status(bikes_docked, capacity) == expected


@pytest.mark.parametrize(
    "bikes_docked, capacity, error_msg",
    [
        (0, 0, "invalid capacity"),       # capacity == 0
        (0, -5, "invalid capacity"),      # capacity < 0
        (-1, 10, "invalid bike count"),   # bikes_docked < 0 (first half of OR True)
        (11, 10, "invalid bike count"),   # bikes_docked > capacity (second half of OR True)
    ],
)
def test_dock_status_error_branches(bikes_docked, capacity, error_msg):
    with pytest.raises(ValueError, match=error_msg):
        dock_status(bikes_docked, capacity)


# --- can_unlock branch tests ---
@pytest.mark.parametrize(
    "account_balance, has_active_ride, age, expected",
    [
        (500, True, 25, False),     # has_active_ride True
        (500, False, 15, False),    # age < 16 True
        (99, False, 16, False),     # 16 <= age < 18, balance < 100
        (100, False, 17, True),     # 16 <= age < 18, balance >= 100
        (49, False, 18, False),     # age >= 18, balance < 50
        (50, False, 18, True),      # age >= 18, balance >= 50
    ],
)
def test_can_unlock_branches(account_balance, has_active_ride, age, expected):
    assert can_unlock(account_balance, has_active_ride, age) is expected