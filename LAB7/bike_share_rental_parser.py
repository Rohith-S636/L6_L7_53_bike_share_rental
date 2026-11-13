def parse_ride_duration(text):
    """
    Converts a ride duration written as HH:MM into minutes.
    Validates input type, colon delimiter, and non-negative numeric bounds.
    """
    if not isinstance(text, str):
        raise ValueError("Duration must be a string")

    cleaned = text.strip()
    parts = cleaned.split(":")
    if len(parts) != 2:
        raise ValueError("Duration must be formatted as HH:MM")

    hours_str, minutes_str = parts[0].strip(), parts[1].strip()
    if not (hours_str.isascii() and hours_str.isdigit() and minutes_str.isascii() and minutes_str.isdigit()):
        raise ValueError("Hours and minutes must contain only ASCII digits")

    hours = int(hours_str)
    minutes = int(minutes_str)
    if minutes >= 60:
        raise ValueError("Minutes must be between 0 and 59")

    return hours * 60 + minutes


def format_station_code(code):
    """
    Formats a station code as ZONE-NUMBER, e.g. 'a12' -> 'A-12'.
    Validates that code starts with an ASCII letter followed by ASCII digits.
    """
    if not isinstance(code, str):
        raise ValueError("Station code must be a string")

    cleaned = code.strip().upper()
    if len(cleaned) < 2:
        raise ValueError("Station code must have at least a zone letter and a number")

    zone, number = cleaned[0], cleaned[1:]
    if not (zone.isascii() and zone.isalpha()):
        raise ValueError("Station zone must be an ASCII letter")
    if not (number.isascii() and number.isdigit()):
        raise ValueError("Station number must contain only digits")

    return f"{zone}-{number}"


def parse_ride_log(line):
    """
    Parses 'bike_type,minutes,subscriber' into a tuple (str, int, bool).
    Validates field count, non-empty bike_type, non-negative integer minutes, and yes/no subscriber flag.
    """
    if not isinstance(line, str):
        raise ValueError("Ride log line must be a string")

    parts = line.split(",")
    if len(parts) != 3:
        raise ValueError("Ride log must have exactly 3 comma-separated fields")

    bike_type = parts[0].strip()
    minutes_str = parts[1].strip()
    subscriber_str = parts[2].strip().lower()

    if not bike_type:
        raise ValueError("Bike type cannot be empty")
    if not (minutes_str.isascii() and minutes_str.isdigit()):
        raise ValueError("Minutes must be a non-negative integer")
    if subscriber_str not in ("yes", "no"):
        raise ValueError("Subscriber field must be 'yes' or 'no'")

    return bike_type, int(minutes_str), subscriber_str == "yes"


def main():
    print("==== Running parse_ride_duration ====")
    value = input("Enter a ride duration as HH:MM (e.g. 01:15): ")
    try:
        print("Duration in minutes:", parse_ride_duration(value))
    except ValueError as e:
        print("Invalid duration:", e)

    print("\n==== Running format_station_code ====")
    value = input("Enter a station code (e.g. a12): ")
    try:
        print("Formatted station code:", format_station_code(value))
    except ValueError as e:
        print("Invalid station code:", e)

    print("\n==== Running parse_ride_log ====")
    value = input("Enter a ride log line as type,minutes,subscriber (e.g. electric,45,yes): ")
    try:
        print("Parsed ride log:", parse_ride_log(value))
    except ValueError as e:
        print("Invalid ride log:", e)


if __name__ == "__main__":
    main()