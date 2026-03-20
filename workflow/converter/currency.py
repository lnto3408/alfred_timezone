"""Currency conversion with caching using Python stdlib."""
import json
import os
import time
import urllib.request
import urllib.error

CACHE_DIR = os.path.expanduser("~/.cache/alfred_converter")
CACHE_TTL = 3600  # 1 hour

from converter.data import ZERO_DECIMAL_CURRENCIES as ZERO_DECIMAL

API_URL = "https://open.er-api.com/v6/latest/{base}"


def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(base):
    return os.path.join(CACHE_DIR, f"rates_{base.upper()}.json")


def _load_cache(base):
    path = _cache_path(base)
    if not os.path.exists(path):
        return None, True
    try:
        with open(path, "r") as f:
            data = json.load(f)
        age = time.time() - data.get("timestamp", 0)
        return data, age > CACHE_TTL
    except (json.JSONDecodeError, OSError):
        return None, True


def _save_cache(base, rates):
    _ensure_cache_dir()
    data = {"timestamp": time.time(), "rates": rates}
    with open(_cache_path(base), "w") as f:
        json.dump(data, f)


def _fetch_rates(base):
    """Fetch exchange rates from API."""
    url = API_URL.format(base=base.upper())
    req = urllib.request.Request(url, headers={"User-Agent": "Alfred-Converter/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("result") == "success":
            return data.get("rates", {})
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        pass
    return None


def get_rates(base):
    """Get exchange rates with caching. Returns (rates_dict, is_stale)."""
    cached, expired = _load_cache(base)

    if not expired and cached:
        return cached["rates"], False

    # Try fetching fresh rates
    fresh = _fetch_rates(base)
    if fresh:
        _save_cache(base, fresh)
        return fresh, False

    # Use stale cache if available
    if cached:
        return cached["rates"], True

    return None, True


def format_amount(amount, currency):
    """Format amount with appropriate decimal places."""
    currency = currency.upper()
    if currency in ZERO_DECIMAL:
        formatted = f"{amount:,.0f}"
    else:
        formatted = f"{amount:,.2f}"
    return formatted


def convert(amount, from_curr, to_curr):
    """Convert currency. Returns list of Alfred items."""
    from converter.alfred import make_item, make_error

    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    rates, is_stale = get_rates(from_curr)

    if rates is None:
        return [make_error("Failed to fetch exchange rates", "Check your internet connection")]

    if to_curr not in rates:
        return [make_error(f"Unknown currency: {to_curr}", f"Cannot convert {from_curr} to {to_curr}")]

    rate = rates[to_curr]
    result = amount * rate

    result_formatted = format_amount(result, to_curr)
    amount_formatted = format_amount(amount, from_curr)

    title = f"{result_formatted} {to_curr}"
    subtitle = f"{amount_formatted} {from_curr} = {result_formatted} {to_curr}"

    if is_stale:
        subtitle += "  (cached rates, may be outdated)"

    subtitle += f"  (1 {from_curr} = {rate:.4f} {to_curr})"

    return [make_item(title, subtitle, arg=result_formatted)]
