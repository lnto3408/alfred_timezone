#!/usr/bin/env python3
"""Alfred Script Filter: ct — timezone conversion + dashboard.

Supports:
  ct                     → dashboard (current time in favorites)
  ct 10am                → dashboard with specific time
  ct 10am utc+7          → 10am at UTC+7, show in local + favorites
  ct 10am gmt+1          → 10am at GMT+1, show in local + favorites
  ct 10am -7             → 10am minus 7 hours (time arithmetic)
  ct 10am +3:30          → 10am plus 3h30m
  ct 12pm to pdt         → single conversion
  ct 12pm to utc+9       → single conversion to offset
  ct 12pm utc+9 to pdt   → from offset to named tz
  ct add tokyo           → add to favorites
  ct remove tokyo        → remove from favorites
"""
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converter.alfred import output, make_item, make_error
from converter.data import resolve_location, search_locations, LOCATIONS, _IDX
from converter import favorites
from converter.timezone import (
    parse_time, get_local_tz, convert as tz_convert,
    resolve_tz, resolve_offset_tz, resolve_bare_offset,
    format_offset, format_date_diff, OFFSET_RE, BARE_OFFSET_RE,
)
from converter.parser import parse, TimezoneQuery

# Time pattern
TIME_RE = re.compile(
    r'^(\d{1,2}(?::\d{2})?\s*(?:am|pm)|\d{1,2}:\d{2}|\d{4})$',
    re.IGNORECASE
)


def _offset_label(dt):
    """Get UTC offset label for a datetime like 'UTC+9'."""
    off = dt.utcoffset()
    if off is None:
        return ""
    return "UTC" + format_offset(off)


def _diff_label(source_dt, target_dt):
    """Compute hour difference between two datetimes."""
    src_off = source_dt.utcoffset() or timedelta(0)
    tgt_off = target_dt.utcoffset() or timedelta(0)
    diff = tgt_off - src_off
    total_minutes = int(diff.total_seconds()) // 60
    hours = total_minutes // 60
    minutes = abs(total_minutes) % 60

    if total_minutes == 0:
        return "same time"
    sign = "+" if total_minutes > 0 else "-"
    if minutes:
        return f"{sign}{abs(hours)}h{minutes:02d}m"
    return f"{sign}{abs(hours)}h"


def show_times(time_str=None, ref_tz=None, ref_label=None):
    """Show time across all favorite timezones.

    Args:
        time_str: time like '10am'. None = current time.
        ref_tz: if set, the time is interpreted in this timezone (e.g., UTC+7)
        ref_label: display label for ref_tz (e.g., 'UTC+7')
    """
    favs = favorites.load()

    if not favs:
        output([make_item(
            "No timezones added yet",
            "Type 'ct add tokyo' to add a timezone",
            valid=False
        )])

    local_tz = get_local_tz()
    now = datetime.now(tz=local_tz)

    # Build source datetime
    if time_str:
        parsed = parse_time(time_str)
        if not parsed:
            output([make_error(f"Cannot parse time: {time_str}", "Try: 10am, 3:30pm, 15:00")])
        hour, minute = parsed
        if ref_tz:
            # Time is in ref_tz
            source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            source_dt = source_dt.replace(tzinfo=ref_tz)
        else:
            source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            source_dt = source_dt.replace(tzinfo=local_tz)
    else:
        source_dt = now

    items = []

    # Header: source time
    if ref_tz and ref_label:
        # Show ref timezone time → local time
        source_fmt = source_dt.strftime("%-I:%M %p")
        local_dt = source_dt.astimezone(local_tz)
        local_fmt = local_dt.strftime("%-I:%M %p")
        local_tz_name = local_dt.strftime("%Z")
        date_note = format_date_diff(source_dt, local_dt)

        items.append(make_item(
            f"{source_fmt} {ref_label}  →  {local_fmt} {local_tz_name}{date_note}",
            f"{ref_label} → Local ({_offset_label(local_dt)})",
            arg=f"{local_fmt} {local_tz_name}",
        ))
        # Use local_dt as base for favorites display
        base_dt = local_dt
    else:
        source_fmt = source_dt.strftime("%-I:%M %p")
        source_tz_name = source_dt.strftime("%Z")
        utc_dt = source_dt.astimezone(timezone.utc)
        utc_fmt = utc_dt.strftime("%-I:%M %p")

        items.append(make_item(
            f"{source_fmt} {source_tz_name}",
            f"Local ({_offset_label(source_dt)})  ·  {utc_fmt} UTC",
            arg=f"{source_fmt} {source_tz_name}",
        ))
        base_dt = source_dt

    # Favorites
    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue

        tz = ZoneInfo(iana)
        target_dt = source_dt.astimezone(tz)
        target_fmt = target_dt.strftime("%-I:%M %p")
        target_tz_name = target_dt.strftime("%Z")

        date_note = format_date_diff(base_dt, target_dt)
        diff = _diff_label(base_dt, target_dt)

        title = f"{target_fmt} {target_tz_name}{date_note}"
        subtitle = f"{loc['city']}, {loc['country']}  ·  {_offset_label(target_dt)}  ·  {diff}"

        items.append(make_item(title, subtitle, arg=f"{target_fmt} {target_tz_name}"))

    output(items)


def show_time_arithmetic(time_str, offset_str):
    """Handle 'ct 10am -7' or 'ct 10am +3:30' — time arithmetic."""
    parsed = parse_time(time_str)
    if not parsed:
        output([make_error(f"Cannot parse time: {time_str}")])

    hour, minute = parsed
    result = resolve_bare_offset(offset_str)
    if not result:
        output([make_error(f"Cannot parse offset: {offset_str}")])

    td, label = result

    local_tz = get_local_tz()
    now = datetime.now(tz=local_tz)
    source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    target_dt = source_dt + td

    source_fmt = source_dt.strftime("%-I:%M %p")
    target_fmt = target_dt.strftime("%-I:%M %p")
    source_tz_name = source_dt.strftime("%Z")
    date_note = format_date_diff(source_dt, target_dt)

    sign = "+" if td.total_seconds() >= 0 else ""
    total_min = int(td.total_seconds()) // 60
    h = total_min // 60
    m = abs(total_min) % 60
    if m:
        delta_label = f"{sign}{h}h{m:02d}m"
    else:
        delta_label = f"{sign}{h}h"

    items = [make_item(
        f"{target_fmt} {source_tz_name}{date_note}",
        f"{source_fmt} {label} = {target_fmt}{date_note}",
        arg=f"{target_fmt}",
    )]

    # Also show in favorites for context
    favs = favorites.load()
    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue
        tz = ZoneInfo(iana)
        fav_dt = target_dt.astimezone(tz)
        fav_fmt = fav_dt.strftime("%-I:%M %p")
        fav_tz_name = fav_dt.strftime("%Z")
        fav_date = format_date_diff(target_dt, fav_dt)

        items.append(make_item(
            f"{fav_fmt} {fav_tz_name}{fav_date}",
            f"{loc['city']}, {loc['country']}  ·  {_offset_label(fav_dt)}",
            arg=f"{fav_fmt} {fav_tz_name}",
        ))

    output(items)


def handle_add(search_query):
    """Search and show locations to add as favorites."""
    if not search_query:
        output([make_item(
            "Search for a city, country, or timezone",
            "e.g., ct add tokyo  |  ct add pdt  |  ct add korea",
            valid=False
        )])

    results = search_locations(search_query)
    current_favs = set(favorites.load())

    if not results:
        output([make_error(f"No results for '{search_query}'", "Try a city, country, or timezone abbreviation")])

    items = []
    for loc in results:
        iana = loc["iana"]
        already = iana in current_favs
        tz_abbrs = "/".join(loc["tz_abbrs"])

        title = f"{loc['city']}, {loc['country']} ({tz_abbrs})"
        if already:
            items.append(make_item(title, "Already added", arg=f"__noop__{iana}", valid=False))
        else:
            subtitle = f"{loc['region']}  ·  {iana}  — Press Enter to add"
            items.append(make_item(title, subtitle, arg=f"__add__{iana}"))

    output(items)


def handle_remove(search_query):
    """Show current favorites for removal."""
    favs = favorites.load()
    if not favs:
        output([make_item("No timezones to remove", "Add some first with 'ct add'", valid=False)])

    items = []
    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue

        if search_query and search_query.lower() not in f"{loc['city']} {loc['country']} {' '.join(loc['tz_abbrs'])}".lower():
            continue

        tz_abbrs = "/".join(loc["tz_abbrs"])
        title = f"{loc['city']}, {loc['country']} ({tz_abbrs})"
        items.append(make_item(title, "Press Enter to remove", arg=f"__remove__{iana}"))

    if not items:
        output([make_error("No matching timezone found", "Check your favorites")])

    output(items)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    query = query.strip()

    # ct → dashboard (current time)
    if not query:
        show_times()

    lower = query.lower()

    # ct add <search>
    if lower.startswith("add"):
        handle_add(query[3:].strip())

    # ct remove / ct rm
    if lower.startswith("remove") or lower.startswith("rm"):
        search = re.sub(r'^(remove|rm)\s*', '', query, flags=re.IGNORECASE).strip()
        handle_remove(search)

    # ct 12pm to pdt / ct 12pm to utc+9 → single conversion
    if " to " in lower or " in " in lower:
        parsed = parse(query)
        if isinstance(parsed, TimezoneQuery):
            items = tz_convert(parsed.time_str, parsed.to_tz, parsed.from_tz)
            output(items)

    # Split query into parts for time + modifier
    parts = query.split()

    if len(parts) >= 2:
        time_part = parts[0]
        modifier = " ".join(parts[1:])

        if TIME_RE.match(time_part):
            # ct 10am -7 / ct 10am +3:30 → time arithmetic
            if BARE_OFFSET_RE.match(modifier):
                show_time_arithmetic(time_part, modifier)

            # ct 10am utc+7 / ct 10am gmt / ct 10am gmt+1 → time at that tz
            if OFFSET_RE.match(modifier):
                result = resolve_offset_tz(modifier)
                if result:
                    ref_tz, ref_label = result
                    show_times(time_part, ref_tz=ref_tz, ref_label=ref_label)

            # ct 10am pdt / ct 10am tokyo → time at that tz
            tz, label = resolve_tz(modifier)
            if tz:
                show_times(time_part, ref_tz=tz, ref_label=label or modifier.upper())

    # ct 10am → dashboard with specific time
    if TIME_RE.match(query):
        show_times(query)

    # ct utc / ct gmt+1 → dashboard showing that tz's current time
    if OFFSET_RE.match(query):
        result = resolve_offset_tz(query)
        if result:
            ref_tz, ref_label = result
            now_ref = datetime.now(tz=ref_tz)
            show_times(ref_tz=ref_tz, ref_label=ref_label)

    # Fallback
    output([make_item(
        "ct — Timezone",
        "ct | ct 10am | ct 10am utc+7 | ct 10am -7 | ct 12pm to pdt | ct add/remove",
        valid=False
    )])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        output([make_error(f"Error: {str(e)}")])
