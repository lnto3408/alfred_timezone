"""Parse user query to detect timezone or currency conversion."""
import re
from collections import namedtuple

from converter.data import resolve_location, _IDX

TimezoneQuery = namedtuple("TimezoneQuery", ["time_str", "from_tz", "to_tz"])
CurrencyQuery = namedtuple("CurrencyQuery", ["amount", "from_curr", "to_curr"])

# Time pattern: 12pm, 3:30pm, 15:00, 0930
TIME_PATTERN = re.compile(
    r'^(\d{1,2}(?::\d{2})?\s*(?:am|pm)|\d{1,2}:\d{2}|\d{4})$',
    re.IGNORECASE
)


def _is_tz(name):
    """Check if a name resolves to a known timezone."""
    return resolve_location(name) is not None or "/" in name or name.upper() == "UTC"


def parse(query):
    """Parse query string. Returns TimezoneQuery, CurrencyQuery, or None."""
    query = query.strip()
    if not query:
        return None

    parts = re.split(r'\s+(?:to|in)\s+', query, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) != 2:
        return None

    left = parts[0].strip()
    right = parts[1].strip()
    if not left or not right:
        return None

    # Try currency first — "1000 krw to usd" should not match as timezone
    curr_result = _try_currency(left, right)
    if curr_result:
        return curr_result

    tz_result = _try_timezone(left, right)
    if tz_result:
        return tz_result

    return None


def _try_timezone(left, right):
    """Try to parse as timezone conversion."""
    if not _is_tz(right):
        return None

    # "12pm to pdt"
    if TIME_PATTERN.match(left):
        return TimezoneQuery(time_str=left, from_tz=None, to_tz=right)

    # "12pm kst to pdt"
    left_parts = left.rsplit(None, 1)
    if len(left_parts) == 2:
        time_part, tz_part = left_parts
        if TIME_PATTERN.match(time_part) and _is_tz(tz_part):
            return TimezoneQuery(time_str=time_part, from_tz=tz_part, to_tz=right)

    return None


def _try_currency(left, right):
    """Try to parse as currency conversion."""
    if not re.match(r'^[a-zA-Z]{3}$', right):
        return None

    m = re.match(r'^([\d,]+\.?\d*)\s+([a-zA-Z]{3})$', left)
    if m:
        amount_str = m.group(1).replace(",", "")
        try:
            amount = float(amount_str)
        except ValueError:
            return None
        return CurrencyQuery(amount=amount, from_curr=m.group(2), to_curr=right)

    return None
