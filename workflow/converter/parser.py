"""Parse user query to detect timezone or currency conversion."""
import re
from collections import namedtuple

TimezoneQuery = namedtuple("TimezoneQuery", ["time_str", "from_tz", "to_tz"])
CurrencyQuery = namedtuple("CurrencyQuery", ["amount", "from_curr", "to_curr"])

# Known timezone abbreviations and city names (for disambiguation)
TZ_KEYWORDS = {
    "PST", "PDT", "PT", "MST", "MDT", "MT", "CST", "CDT", "CT",
    "EST", "EDT", "ET", "HST", "AKST", "AKDT",
    "GMT", "BST", "CET", "CEST", "EET", "EEST", "WET", "WEST",
    "JST", "KST", "HKT", "SGT", "IST", "ICT", "PHT", "WIB", "TWT",
    "AEST", "AEDT", "ACST", "ACDT", "AWST", "NZST", "NZDT",
    "UTC",
    # Cities
    "SEOUL", "TOKYO", "LONDON", "PARIS", "BERLIN", "NYC", "NEWYORK",
    "LA", "SF", "CHICAGO", "DENVER", "SYDNEY", "MELBOURNE", "AUCKLAND",
    "SINGAPORE", "HONGKONG", "HK", "SHANGHAI", "BEIJING", "MUMBAI",
    "DELHI", "BANGKOK", "TAIPEI", "DUBAI", "HAWAII",
}

# Time pattern: 12pm, 3:30pm, 15:00, 0930
TIME_PATTERN = re.compile(
    r'^(\d{1,2}(?::\d{2})?\s*(?:am|pm)|\d{1,2}:\d{2}|\d{4})$',
    re.IGNORECASE
)


def parse(query):
    """Parse query string. Returns TimezoneQuery, CurrencyQuery, or None."""
    query = query.strip()
    if not query:
        return None

    # Split on " to " or " in " (case-insensitive)
    parts = re.split(r'\s+(?:to|in)\s+', query, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) != 2:
        return None

    left = parts[0].strip()
    right = parts[1].strip()

    if not left or not right:
        return None

    # Try timezone: left should be a time, right should be a timezone
    # Also support: "12pm kst to pdt" (with source timezone)
    tz_result = _try_timezone(left, right)
    if tz_result:
        return tz_result

    # Try currency: left should be "amount currency", right should be currency
    curr_result = _try_currency(left, right)
    if curr_result:
        return curr_result

    return None


def _try_timezone(left, right):
    """Try to parse as timezone conversion."""
    # Check if right side is a timezone
    if right.upper().replace(" ", "") not in TZ_KEYWORDS:
        # Try as IANA name
        if "/" not in right:
            return None

    # Case 1: "12pm to pdt" - time (to) timezone
    if TIME_PATTERN.match(left):
        return TimezoneQuery(time_str=left, from_tz=None, to_tz=right)

    # Case 2: "12pm kst to pdt" - time from_tz (to) to_tz
    # Split left into time + timezone
    left_parts = left.rsplit(None, 1)
    if len(left_parts) == 2:
        time_part, tz_part = left_parts
        if TIME_PATTERN.match(time_part) and tz_part.upper() in TZ_KEYWORDS:
            return TimezoneQuery(time_str=time_part, from_tz=tz_part, to_tz=right)

    return None


def _try_currency(left, right):
    """Try to parse as currency conversion."""
    # Right side should be a currency code (3 letters)
    if not re.match(r'^[a-zA-Z]{3}$', right):
        return None

    # Left side: "1000 krw", "1,000.50 usd", "50 eur"
    m = re.match(r'^([\d,]+\.?\d*)\s+([a-zA-Z]{3})$', left)
    if m:
        amount_str = m.group(1).replace(",", "")
        try:
            amount = float(amount_str)
        except ValueError:
            return None
        return CurrencyQuery(amount=amount, from_curr=m.group(2), to_curr=right)

    return None
