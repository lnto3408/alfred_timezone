"""Manage favorites for ct (timezones) and cc (currencies) + settings."""
import json
import os

CONFIG_DIR = os.path.expanduser("~/.config/alfred_converter")
TZ_PATH = os.path.join(CONFIG_DIR, "favorites.json")
CURR_PATH = os.path.join(CONFIG_DIR, "currencies.json")
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.json")

# Predefined time format presets
TIME_FORMATS = [
    {"id": "12h",      "label": "3:30 PM",               "fmt": "%-I:%M %p"},
    {"id": "12h_tz",   "label": "3:30 PM PST",           "fmt": "%-I:%M %p %Z"},
    {"id": "24h",      "label": "15:30",                  "fmt": "%H:%M"},
    {"id": "24h_tz",   "label": "15:30 PST",             "fmt": "%H:%M %Z"},
    {"id": "full",     "label": "2026-03-20 15:30 PST",  "fmt": "%Y-%m-%d %H:%M %Z"},
    {"id": "date_12h", "label": "Mar 20, 3:30 PM PST",   "fmt": "%b %-d, %-I:%M %p %Z"},
    {"id": "iso",      "label": "2026-03-20T15:30+09:00", "fmt": "%Y-%m-%dT%H:%M%z"},
]

DEFAULT_FORMAT = "12h_tz"


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


# Settings
def _load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {}
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_settings(settings):
    _ensure_dir()
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)


def get_time_format():
    """Get current time format string."""
    settings = _load_settings()
    fmt_id = settings.get("time_format", DEFAULT_FORMAT)

    # Check presets
    for preset in TIME_FORMATS:
        if preset["id"] == fmt_id:
            return preset["fmt"]

    # Custom format stored directly
    custom = settings.get("time_format_custom")
    if custom:
        return custom

    # Fallback
    return "%-I:%M %p %Z"


def set_time_format(fmt_id):
    """Set time format by preset ID."""
    settings = _load_settings()
    settings["time_format"] = fmt_id
    if "time_format_custom" in settings:
        del settings["time_format_custom"]
    _save_settings(settings)


def set_custom_time_format(fmt_str):
    """Set a custom strftime format string."""
    settings = _load_settings()
    settings["time_format"] = "custom"
    settings["time_format_custom"] = fmt_str
    _save_settings(settings)


def get_time_format_id():
    """Get current format ID."""
    settings = _load_settings()
    return settings.get("time_format", DEFAULT_FORMAT)


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
