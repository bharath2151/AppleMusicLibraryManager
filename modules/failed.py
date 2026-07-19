import json
from pathlib import Path

from modules.config import load_config

config = load_config()

FAILED_JSON = Path(config["failed_songs_path"])


def load_failed_songs():
    if not FAILED_JSON.exists():
        return []

    try:
        with open(FAILED_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def failed_count():
    return len(load_failed_songs())


def get_failed_songs():
    return load_failed_songs()