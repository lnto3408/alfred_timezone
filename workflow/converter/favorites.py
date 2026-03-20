"""Manage favorite timezones for the ct command."""
import json
import os

FAVORITES_PATH = os.path.expanduser("~/.config/alfred_converter/favorites.json")


def _ensure_dir():
    os.makedirs(os.path.dirname(FAVORITES_PATH), exist_ok=True)


def load():
    """Load favorite IANA timezone list. Returns list of iana strings."""
    if not os.path.exists(FAVORITES_PATH):
        return []
    try:
        with open(FAVORITES_PATH, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save(favorites):
    """Save favorite IANA timezone list."""
    _ensure_dir()
    with open(FAVORITES_PATH, "w") as f:
        json.dump(favorites, f, indent=2)


def add(iana):
    """Add a timezone to favorites. Returns True if added, False if already exists."""
    favs = load()
    if iana in favs:
        return False
    favs.append(iana)
    save(favs)
    return True


def remove(iana):
    """Remove a timezone from favorites. Returns True if removed."""
    favs = load()
    if iana not in favs:
        return False
    favs.remove(iana)
    save(favs)
    return True
