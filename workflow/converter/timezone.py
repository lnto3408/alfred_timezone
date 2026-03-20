"""Timezone conversion with DST awareness using Python stdlib."""
import os
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Map common abbreviations to IANA timezone names.
# For ambiguous ones (IST, CST), we pick the most common usage.
TZ_MAP = {
    # US
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "PT": "America/Los_Angeles",
    "MST": "America/Denver",
    "MDT": "America/Denver",
    "MT": "America/Denver",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "CT": "America/Chicago",
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "ET": "America/New_York",
    "HST": "Pacific/Honolulu",
    "AKST": "America/Anchorage",
    "AKDT": "America/Anchorage",
    # Europe
    "GMT": "Europe/London",
    "BST": "Europe/London",
    "CET": "Europe/Berlin",
    "CEST": "Europe/Berlin",
    "EET": "Europe/Bucharest",
    "EEST": "Europe/Bucharest",
    "WET": "Europe/Lisbon",
    "WEST": "Europe/Lisbon",
    # Asia
    "JST": "Asia/Tokyo",
    "KST": "Asia/Seoul",
    "CST_CN": "Asia/Shanghai",
    "HKT": "Asia/Hong_Kong",
    "SGT": "Asia/Singapore",
    "IST": "Asia/Kolkata",
    "ICT": "Asia/Bangkok",
    "PHT": "Asia/Manila",
    "WIB": "Asia/Jakarta",
    "TWT": "Asia/Taipei",
    # Australia / NZ
    "AEST": "Australia/Sydney",
    "AEDT": "Australia/Sydney",
    "ACST": "Australia/Adelaide",
    "ACDT": "Australia/Adelaide",
    "AWST": "Australia/Perth",
    "NZST": "Pacific/Auckland",
    "NZDT": "Pacific/Auckland",
    # UTC
    "UTC": "UTC",
}

# Also support city/region names
CITY_MAP = {
    "SEOUL": "Asia/Seoul",
    "TOKYO": "Asia/Tokyo",
    "LONDON": "Europe/London",
    "PARIS": "Europe/Paris",
    "BERLIN": "Europe/Berlin",
    "NYC": "America/New_York",
    "NEWYORK": "America/New_York",
    "LA": "America/Los_Angeles",
    "SF": "America/Los_Angeles",
    "CHICAGO": "America/Chicago",
    "DENVER": "America/Denver",
    "SYDNEY": "Australia/Sydney",
    "MELBOURNE": "Australia/Melbourne",
    "AUCKLAND": "Pacific/Auckland",
    "SINGAPORE": "Asia/Singapore",
    "HONGKONG": "Asia/Hong_Kong",
    "HK": "Asia/Hong_Kong",
    "SHANGHAI": "Asia/Shanghai",
    "BEIJING": "Asia/Shanghai",
    "MUMBAI": "Asia/Kolkata",
    "DELHI": "Asia/Kolkata",
    "BANGKOK": "Asia/Bangkok",
    "TAIPEI": "Asia/Taipei",
    "DUBAI": "Asia/Dubai",
    "HAWAII": "Pacific/Honolulu",
}


def get_local_tz():
    """Get local IANA timezone from macOS symlink."""
    try:
        link = os.readlink("/etc/localtime")
        # e.g., /var/db/timezone/zoneinfo/Asia/Seoul
        parts = link.split("/zoneinfo/")
        if len(parts) == 2:
            return ZoneInfo(parts[1])
    except (OSError, KeyError):
        pass
    # Fallback
    return datetime.now().astimezone().tzinfo


def resolve_tz(name):
    """Resolve a timezone name/abbreviation to a ZoneInfo object."""
    upper = name.upper().strip().replace(" ", "")

    # Check abbreviation map
    if upper in TZ_MAP:
        return ZoneInfo(TZ_MAP[upper])

    # Check city map
    if upper in CITY_MAP:
        return ZoneInfo(CITY_MAP[upper])

    # Try as direct IANA name (e.g., "America/New_York")
    try:
        return ZoneInfo(name)
    except (KeyError, ValueError):
        pass

    return None


def parse_time(time_str):
    """Parse a time string like '12pm', '3:30pm', '15:00', '1430'."""
    s = time_str.strip().lower()

    # 12-hour with am/pm: "12pm", "3:30pm", "3:30 pm", "12 am"
    m = re.match(r'^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$', s)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2)) if m.group(2) else 0
        ampm = m.group(3)
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        return hour, minute

    # 24-hour with colon: "15:00", "9:30"
    m = re.match(r'^(\d{1,2}):(\d{2})$', s)
    if m:
        return int(m.group(1)), int(m.group(2))

    # 4-digit 24h: "1430", "0900"
    m = re.match(r'^(\d{2})(\d{2})$', s)
    if m:
        return int(m.group(1)), int(m.group(2))

    return None


def convert(time_str, to_tz_str, from_tz_str=None):
    """Convert time between timezones. Returns list of Alfred items."""
    from converter.alfred import make_item, make_error

    parsed = parse_time(time_str)
    if not parsed:
        return [make_error(f"Cannot parse time: {time_str}", "Try formats like 12pm, 3:30pm, 15:00")]

    hour, minute = parsed

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return [make_error(f"Invalid time: {hour}:{minute:02d}")]

    to_tz = resolve_tz(to_tz_str)
    if not to_tz:
        return [make_error(f"Unknown timezone: {to_tz_str}", "Try PST, EST, JST, KST, UTC, etc.")]

    if from_tz_str:
        from_tz = resolve_tz(from_tz_str)
        if not from_tz:
            return [make_error(f"Unknown timezone: {from_tz_str}")]
    else:
        from_tz = get_local_tz()

    now = datetime.now()
    source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    source_dt = source_dt.replace(tzinfo=from_tz)
    target_dt = source_dt.astimezone(to_tz)

    # Format output
    source_fmt = source_dt.strftime("%-I:%M %p").lstrip("0")
    target_fmt = target_dt.strftime("%-I:%M %p").lstrip("0")
    source_tz_name = source_dt.strftime("%Z")
    target_tz_name = target_dt.strftime("%Z")

    # Show date if day changes
    date_note = ""
    if source_dt.date() != target_dt.date():
        diff = (target_dt.date() - source_dt.date()).days
        if diff == 1:
            date_note = " (next day)"
        elif diff == -1:
            date_note = " (previous day)"
        else:
            date_note = f" ({target_dt.strftime('%b %-d')})"

    title = f"{target_fmt} {target_tz_name}{date_note}"
    subtitle = f"{source_fmt} {source_tz_name} → {target_fmt} {target_tz_name}"

    if date_note:
        subtitle += f"  {date_note}"

    return [make_item(title, subtitle, arg=f"{target_fmt} {target_tz_name}")]
