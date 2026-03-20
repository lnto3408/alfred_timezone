"""Timezone conversion with DST awareness using Python stdlib."""
import os
import re
import time as _time
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

# Patterns for log/ISO timestamps
_DATETIME_PATTERNS = [
    # ISO 8601 with T separator and optional fractional seconds and offset
    # 2026-03-07T07:49:58.720Z, 2026-03-07T07:49:58+09:00, 2026-03-07T07:49:58.720+0900
    (re.compile(
        r'^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(?:\.(\d+))?\s*'
        r'(Z|[+-]\d{2}:?\d{2})?$'
    ), "iso"),

    # Compact ISO: 20260307T074958
    (re.compile(
        r'^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})$'
    ), "compact"),

    # Apache/nginx: 07/Mar/2026:07:49:58 +0900
    (re.compile(
        r'^(\d{2})/(\w{3})/(\d{4}):(\d{2}:\d{2}:\d{2})\s*([+-]\d{4})?$'
    ), "apache"),

    # Human readable: Mar 7, 2026 07:49:58
    (re.compile(
        r'^(\w{3})\s+(\d{1,2}),?\s+(\d{4})\s+(\d{2}:\d{2}:\d{2})(?:\.(\d+))?$'
    ), "human"),

    # Date + time: 2026-03-07 07:49:58 (without T)
    # Already covered by iso pattern above (allows space)

    # Date only: 2026-03-07
    (re.compile(r'^(\d{4}-\d{2}-\d{2})$'), "date_only"),
]

_MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


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
    """Parse an offset string like '+9', '-6', '+5:30', '+530' into timedelta."""
    if not offset_str:
        return timedelta(0), ""

    sign = 1 if offset_str[0] == '+' else -1
    rest = offset_str[1:]

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
    """Try to resolve name as UTC/GMT offset. Returns (tzinfo, label) or None."""
    m = OFFSET_RE.match(name.strip())
    if not m:
        return None

    base = m.group(1).upper()
    offset_part = m.group(2) or ""

    td, _ = parse_offset(offset_part) if offset_part else (timedelta(0), "")
    tz = timezone(td)

    if offset_part:
        label = f"{base}{offset_part}"
    else:
        label = base

    return tz, label.upper()


def resolve_bare_offset(name):
    """Try to resolve as bare offset like +9, -6, +5:30."""
    m = BARE_OFFSET_RE.match(name.strip())
    if not m:
        return None
    td, label = parse_offset(m.group(1))
    return td, label


def _parse_tz_offset_str(s):
    """Parse a timezone offset string from a timestamp. Returns timezone or None."""
    if not s:
        return None
    if s == "Z":
        return timezone.utc
    # +0900, +09:00, -05:00, -0500
    clean = s.replace(":", "")
    sign = 1 if clean[0] == '+' else -1
    hours = int(clean[1:3])
    minutes = int(clean[3:5]) if len(clean) >= 5 else 0
    return timezone(timedelta(hours=sign * hours, minutes=sign * minutes))


def parse_datetime(s):
    """Parse various datetime/timestamp formats from logs.

    Returns (datetime_with_tz, original_str) or None.
    If the timestamp has no timezone, assumes local timezone.
    """
    s = s.strip()

    # Unix timestamp (seconds: 10 digits, millis: 13 digits)
    if re.match(r'^\d{10,13}$', s):
        ts = int(s)
        if ts > 9999999999:  # milliseconds
            ts = ts / 1000.0
        try:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return dt, s
        except (OSError, OverflowError, ValueError):
            return None

    for pattern, fmt_type in _DATETIME_PATTERNS:
        m = pattern.match(s)
        if not m:
            continue

        try:
            if fmt_type == "iso":
                date_str = m.group(1)
                time_str = m.group(2)
                # frac = m.group(3)  # fractional seconds (ignored for display)
                tz_str = m.group(4)

                dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                tz_info = _parse_tz_offset_str(tz_str)
                if tz_info:
                    dt = dt.replace(tzinfo=tz_info)
                else:
                    dt = dt.replace(tzinfo=get_local_tz())
                return dt, s

            elif fmt_type == "compact":
                y, mo, d, h, mi, sec = m.groups()
                dt = datetime(int(y), int(mo), int(d), int(h), int(mi), int(sec),
                              tzinfo=get_local_tz())
                return dt, s

            elif fmt_type == "apache":
                day, month_str, year, time_str, tz_str = m.groups()
                month = _MONTH_MAP.get(month_str.lower())
                if not month:
                    continue
                dt = datetime.strptime(f"{year}-{month:02d}-{int(day):02d} {time_str}",
                                       "%Y-%m-%d %H:%M:%S")
                tz_info = _parse_tz_offset_str(tz_str)
                if tz_info:
                    dt = dt.replace(tzinfo=tz_info)
                else:
                    dt = dt.replace(tzinfo=get_local_tz())
                return dt, s

            elif fmt_type == "human":
                month_str, day, year, time_str = m.group(1), m.group(2), m.group(3), m.group(4)
                month = _MONTH_MAP.get(month_str.lower())
                if not month:
                    continue
                dt = datetime.strptime(f"{year}-{month:02d}-{int(day):02d} {time_str}",
                                       "%Y-%m-%d %H:%M:%S")
                dt = dt.replace(tzinfo=get_local_tz())
                return dt, s

            elif fmt_type == "date_only":
                dt = datetime.strptime(m.group(1), "%Y-%m-%d")
                dt = dt.replace(tzinfo=get_local_tz())
                return dt, s

        except (ValueError, TypeError):
            continue

    return None


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
    Returns (tzinfo, label) tuple.
    """
    result = resolve_offset_tz(name)
    if result:
        return result

    iana = get_iana(name)
    if iana:
        try:
            zi = ZoneInfo(iana)
            return zi, None
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
    """Convert time between timezones. Returns list of Alfred items.
    Supports both simple times (12pm) and full timestamps (2026-03-07T07:49:58).
    """
    from converter.alfred import make_item, make_error
    from converter import favorites

    # Try full datetime first
    dt_result = parse_datetime(time_str)
    if dt_result:
        source_dt, original = dt_result

        # If from_tz specified, override the source timezone
        if from_tz_str:
            from_tz, from_label = resolve_tz(from_tz_str)
            if not from_tz:
                return [make_error(f"Unknown timezone: {from_tz_str}")]
            source_dt = source_dt.replace(tzinfo=from_tz)

        to_tz, to_label = resolve_tz(to_tz_str)
        if not to_tz:
            return [make_error(f"Unknown timezone: {to_tz_str}")]

        target_dt = source_dt.astimezone(to_tz)

        source_tz_name = source_dt.strftime("%Z") or "Local"
        target_tz_name = to_label or target_dt.strftime("%Z")

        copy_fmt = favorites.get_time_format()
        date_note = format_date_diff(source_dt, target_dt)

        title = f"{target_dt.strftime('%-I:%M %p')} {target_tz_name}  ({target_dt.strftime('%b %-d')}){date_note}"
        subtitle = f"{source_dt.strftime('%Y-%m-%d %-I:%M %p')} {source_tz_name} → {target_dt.strftime('%-I:%M %p')} {target_tz_name}"

        return [make_item(title, subtitle, arg=target_dt.strftime(copy_fmt))]

    # Fall back to simple time
    parsed = parse_time(time_str)
    if not parsed:
        return [make_error(f"Cannot parse: {time_str}", "Try: 12pm, 15:00, 2026-03-07T07:49:58")]

    hour, minute = parsed
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return [make_error(f"Invalid time: {hour}:{minute:02d}")]

    to_tz, to_label = resolve_tz(to_tz_str)
    if not to_tz:
        return [make_error(f"Unknown timezone: {to_tz_str}")]

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

    copy_fmt = favorites.get_time_format()
    title = f"{target_fmt} {target_tz_name}{date_note}"
    subtitle = f"{source_fmt} {source_tz_name} → {target_fmt} {target_tz_name}"
    if date_note:
        subtitle += f"  {date_note}"

    return [make_item(title, subtitle, arg=target_dt.strftime(copy_fmt))]
