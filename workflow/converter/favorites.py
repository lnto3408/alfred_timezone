"""Manage favorites for ct (timezones) and cc (currencies)."""
import json
import os

CONFIG_DIR = os.path.expanduser("~/.config/alfred_converter")
TZ_PATH = os.path.join(CONFIG_DIR, "favorites.json")
CURR_PATH = os.path.join(CONFIG_DIR, "currencies.json")


def _ensure_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def _load(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save(path, items):
    _ensure_dir()
    with open(path, "w") as f:
        json.dump(items, f, indent=2)


def _add(path, item):
    items = _load(path)
    if item in items:
        return False
    items.append(item)
    _save(path, items)
    return True


def _remove(path, item):
    items = _load(path)
    if item not in items:
        return False
    items.remove(item)
    _save(path, items)
    return True


# Timezone favorites
def load():
    return _load(TZ_PATH)

def save(favorites):
    _save(TZ_PATH, favorites)

def add(iana):
    return _add(TZ_PATH, iana)

def remove(iana):
    return _remove(TZ_PATH, iana)


# Currency favorites
def load_currencies():
    return _load(CURR_PATH)

def save_currencies(currencies):
    _save(CURR_PATH, currencies)

def add_currency(code):
    return _add(CURR_PATH, code.upper())

def remove_currency(code):
    return _remove(CURR_PATH, code.upper())
