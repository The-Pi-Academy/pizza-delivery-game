import base64
import json
import os

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".save")


def _fmt(seconds: float) -> str:
    """Format a time in seconds as M:SS.hh"""
    minutes           = int(seconds) // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:05.2f}"


def format_time(seconds: float) -> str:
    return _fmt(seconds)


def load_best_times(num_levels: int) -> list:
    if not os.path.isfile(SAVE_FILE):
        return [None] * num_levels
    try:
        with open(SAVE_FILE, "rb") as f:
            decoded_data = base64.b64decode(f.read())
        saved_times = json.loads(decoded_data)
        result = list(saved_times[:num_levels])
        while len(result) < num_levels:
            result.append(None)
        return result
    except Exception:
        return [None] * num_levels


def save_best_times(best_times: list) -> None:
    encoded_data = json.dumps(best_times).encode()
    with open(SAVE_FILE, "wb") as f:
        f.write(base64.b64encode(encoded_data))
