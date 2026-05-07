import base64
import json
import os

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".save")


def _fmt(seconds: float) -> str:
    """Format a time in seconds as M:SS.hh"""
    mins  = int(seconds) // 60
    secs  = seconds % 60
    return f"{mins}:{secs:05.2f}"


def format_time(seconds: float) -> str:
    return _fmt(seconds)


def load_best_times(num_levels: int) -> list:
    if not os.path.isfile(SAVE_FILE):
        return [None] * num_levels
    try:
        with open(SAVE_FILE, "rb") as f:
            raw = base64.b64decode(f.read())
        saved = json.loads(raw)
        result = list(saved[:num_levels])
        while len(result) < num_levels:
            result.append(None)
        return result
    except Exception:
        return [None] * num_levels


def save_best_times(best_times: list) -> None:
    raw = json.dumps(best_times).encode()
    with open(SAVE_FILE, "wb") as f:
        f.write(base64.b64encode(raw))
