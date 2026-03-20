"""Timezone conversion with DST awareness using Python stdlib."""
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from converter.data import get_iana


def get_local_tz():
    """Get local IANA timezone from macOS symlink."""
    try:
        link = os.readlink("/etc/localtime")
        parts = link.split("/zoneinfo/")
        if len(parts) == 2:
            return ZoneInfo(parts[1])
    except (OSError, KeyError):
        pass
    return datetime.now().astimezone().tzinfo


def parse_time(time_str):
    """Parse a time string like '12pm', '3:30pm', '15:00', '1430'."""
    s = time_str.strip().lower()

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

    m = re.match(r'^(\d{1,2}):(\d{2})$', s)
    if m:
        return int(m.group(1)), int(m.group(2))

    m = re.match(r'^(\d{2})(\d{2})$', s)
    if m:
        return int(m.group(1)), int(m.group(2))

    return None


def resolve_tz(name):
    """Resolve a timezone name/abbreviation to a ZoneInfo object."""
    iana = get_iana(name)
    if iana:
        try:
            return ZoneInfo(iana)
        except (KeyError, ValueError):
            pass
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
        return [make_error(f"Unknown timezone: {to_tz_str}", "Try PST, EST, JST, KST, UTC, tokyo, london, etc.")]

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

    source_fmt = source_dt.strftime("%-I:%M %p")
    target_fmt = target_dt.strftime("%-I:%M %p")
    source_tz_name = source_dt.strftime("%Z")
    target_tz_name = target_dt.strftime("%Z")

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
