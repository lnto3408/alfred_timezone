"""Timezone conversion with DST awareness using Python stdlib."""
import os
import re
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from converter.data import get_iana

# Pattern for UTC/GMT offsets: utc, gmt, utc+9, gmt-6, utc+5:30, gmt+5:45
OFFSET_RE = re.compile(
    r'^(utc|gmt)([+-]\d{1,2}(?::?\d{2})?)?$',
    re.IGNORECASE
)

# Pattern for bare offsets: +9, -6, +5:30
BARE_OFFSET_RE = re.compile(
    r'^([+-]\d{1,2}(?::?\d{2})?)$'
)


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


def parse_offset(offset_str):
    """Parse an offset string like '+9', '-6', '+5:30', '+530' into timedelta.
    Returns (timedelta, label) or None.
    """
    if not offset_str:
        return timedelta(0), ""

    sign = 1 if offset_str[0] == '+' else -1
    rest = offset_str[1:]

    # +5:30 or +530
    if ':' in rest:
        parts = rest.split(':')
        hours = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 0
    elif len(rest) >= 3:
        hours = int(rest[:-2])
        minutes = int(rest[-2:])
    else:
        hours = int(rest)
        minutes = 0

    td = timedelta(hours=sign * hours, minutes=sign * minutes)
    return td, offset_str


def resolve_offset_tz(name):
    """Try to resolve name as UTC/GMT offset. Returns (tzinfo, label) or None.

    Supports: utc, gmt, utc+9, gmt-6, utc+5:30
    """
    m = OFFSET_RE.match(name.strip())
    if not m:
        return None

    base = m.group(1).upper()
    offset_part = m.group(2) or ""

    td, _ = parse_offset(offset_part) if offset_part else (timedelta(0), "")
    tz = timezone(td)

    # Build label: UTC+9, GMT-6, UTC+5:30
    if offset_part:
        label = f"{base}{offset_part}"
    else:
        label = base

    return tz, label.upper()


def resolve_bare_offset(name):
    """Try to resolve as bare offset like +9, -6, +5:30.
    Returns (timedelta, label) or None.
    """
    m = BARE_OFFSET_RE.match(name.strip())
    if not m:
        return None
    td, label = parse_offset(m.group(1))
    return td, label


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
    """Resolve a timezone name/abbreviation/offset to a tzinfo object.
    Returns (tzinfo, label) tuple. label is display name like 'PST', 'UTC+9'.
    """
    # Try UTC/GMT offset first
    result = resolve_offset_tz(name)
    if result:
        return result

    # Try IANA/abbreviation/city
    iana = get_iana(name)
    if iana:
        try:
            zi = ZoneInfo(iana)
            return zi, None  # label will be derived from strftime %Z
        except (KeyError, ValueError):
            pass

    return None, None


def format_offset(td):
    """Format a timedelta as UTC offset string like +9:00, -5:30."""
    total_seconds = int(td.total_seconds())
    sign = "+" if total_seconds >= 0 else "-"
    total_seconds = abs(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    if minutes:
        return f"{sign}{hours}:{minutes:02d}"
    return f"{sign}{hours}"


def format_date_diff(source_dt, target_dt):
    """Format date difference note."""
    if source_dt.date() == target_dt.date():
        return ""
    diff = (target_dt.date() - source_dt.date()).days
    if diff == 1:
        return " (tomorrow)"
    elif diff == -1:
        return " (yesterday)"
    else:
        return f" ({target_dt.strftime('%b %-d')})"


def convert(time_str, to_tz_str, from_tz_str=None):
    """Convert time between timezones. Returns list of Alfred items."""
    from converter.alfred import make_item, make_error

    parsed = parse_time(time_str)
    if not parsed:
        return [make_error(f"Cannot parse time: {time_str}", "Try formats like 12pm, 3:30pm, 15:00")]

    hour, minute = parsed
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return [make_error(f"Invalid time: {hour}:{minute:02d}")]

    to_tz, to_label = resolve_tz(to_tz_str)
    if not to_tz:
        return [make_error(f"Unknown timezone: {to_tz_str}", "Try PST, UTC+9, GMT-6, tokyo, etc.")]

    if from_tz_str:
        from_tz, from_label = resolve_tz(from_tz_str)
        if not from_tz:
            return [make_error(f"Unknown timezone: {from_tz_str}")]
    else:
        from_tz = get_local_tz()
        from_label = None

    now = datetime.now()
    source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    source_dt = source_dt.replace(tzinfo=from_tz)
    target_dt = source_dt.astimezone(to_tz)

    source_fmt = source_dt.strftime("%-I:%M %p")
    target_fmt = target_dt.strftime("%-I:%M %p")
    source_tz_name = from_label or source_dt.strftime("%Z")
    target_tz_name = to_label or target_dt.strftime("%Z")

    date_note = format_date_diff(source_dt, target_dt)

    title = f"{target_fmt} {target_tz_name}{date_note}"
    subtitle = f"{source_fmt} {source_tz_name} → {target_fmt} {target_tz_name}"
    if date_note:
        subtitle += f"  {date_note}"

    return [make_item(title, subtitle, arg=f"{target_fmt} {target_tz_name}")]
