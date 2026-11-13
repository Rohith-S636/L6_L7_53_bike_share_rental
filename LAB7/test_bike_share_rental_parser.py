from hypothesis import given, strategies as st
from bike_share_rental_parser import parse_ride_duration, format_station_code, parse_ride_log


@given(st.text() | st.none())
def test_parse_ride_duration_no_crash(s):
    try:
        result = parse_ride_duration(s)
        assert isinstance(result, int) and result >= 0
    except ValueError:
        pass
    except Exception as e:
        assert False, f"parse_ride_duration crashed unexpectedly with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_format_station_code_no_crash(s):
    try:
        result = format_station_code(s)
        assert isinstance(result, str) and "-" in result
    except ValueError:
        pass
    except Exception as e:
        assert False, f"format_station_code crashed unexpectedly with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_ride_log_no_crash(s):
    try:
        result = parse_ride_log(s)
        assert isinstance(result, tuple) and len(result) == 3
        assert isinstance(result[0], str)
        assert isinstance(result[1], int)
        assert isinstance(result[2], bool)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"parse_ride_log crashed unexpectedly with {type(e).__name__}: {e}"