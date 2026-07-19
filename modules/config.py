import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            "config.json not found. Please create it before running AMLM."
        )

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        raise ValueError(
            "config.json contains invalid JSON."
        )
config = load_config()