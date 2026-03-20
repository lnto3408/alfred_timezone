#!/usr/bin/env python3
"""Alfred Script Filter: ct — timezone conversion + dashboard.

Supports:
  ct                     → dashboard (current time in favorites)
  ct 10am                → dashboard with specific time
  ct +1 / ct -3          → current time +/- hours (arithmetic)
  ct 10am -7             → 10am minus 7 hours
  ct 10am +3:30          → 10am plus 3h30m
  ct utc+3 / ct gmt-6    → show local → that tz + favorites
  ct 10am utc+7          → 10am at UTC+7, show as local + favorites
  ct 12pm to pdt         → single conversion
  ct 12pm to utc+9       → single conversion to offset
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

TIME_RE = re.compile(
    r'^(\d{1,2}(?::\d{2})?\s*(?:am|pm)|\d{1,2}:\d{2}|\d{4})$',
    re.IGNORECASE
)


def _offset_label(dt):
    """UTC offset label like 'UTC+9'."""
    off = dt.utcoffset()
    if off is None:
        return ""
    return "UTC" + format_offset(off)


def _diff_label(source_dt, target_dt):
    """Hour difference between two datetimes."""
    src_off = source_dt.utcoffset() or timedelta(0)
    tgt_off = target_dt.utcoffset() or timedelta(0)
    total_minutes = int((tgt_off - src_off).total_seconds()) // 60
    if total_minutes == 0:
        return "same time"
    sign = "+" if total_minutes > 0 else "-"
    h = abs(total_minutes) // 60
    m = abs(total_minutes) % 60
    if m:
        return f"{sign}{h}h{m:02d}m"
    return f"{sign}{h}h"


def _fmt(dt):
    """Format datetime as '3:04 PM'."""
    return dt.strftime("%-I:%M %p")


def _tz_name(dt, label=None):
    """Get tz display name."""
    return label or dt.strftime("%Z")


def show_dashboard(time_str=None, ref_tz=None, ref_label=None):
    """Show time across all favorite timezones.

    - No ref_tz: local time as base
    - ref_tz set + time_str: that time IS in ref_tz → convert to local + favs
    - ref_tz set + no time_str: show current local → ref_tz + favs
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
    items = []

    if ref_tz and time_str:
        # "ct 10am utc+7" → 10am IS at ref_tz, convert to local
        parsed = parse_time(time_str)
        if not parsed:
            output([make_error(f"Cannot parse time: {time_str}")])
        hour, minute = parsed
        source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        source_dt = source_dt.replace(tzinfo=ref_tz)
        local_dt = source_dt.astimezone(local_tz)
        date_note = format_date_diff(source_dt, local_dt)

        # Header: base (input) → local
        items.append(make_item(
            f"{_fmt(source_dt)} {ref_label}  →  {_fmt(local_dt)} {local_dt.strftime('%Z')}{date_note}",
            f"{ref_label} → Local ({_offset_label(local_dt)})",
            arg=f"{_fmt(local_dt)} {local_dt.strftime('%Z')}",
        ))
        base_dt = source_dt

    elif ref_tz and not time_str:
        # "ct utc+3" → show current local → ref_tz
        target_dt = now.astimezone(ref_tz)
        date_note = format_date_diff(now, target_dt)

        # Header: local (base) → ref_tz (target)
        items.append(make_item(
            f"{_fmt(now)} {now.strftime('%Z')}  →  {_fmt(target_dt)} {ref_label}{date_note}",
            f"Local ({_offset_label(now)}) → {ref_label}",
            arg=f"{_fmt(target_dt)} {ref_label}",
        ))
        base_dt = now

    else:
        # "ct" or "ct 10am" → local time base
        if time_str:
            parsed = parse_time(time_str)
            if not parsed:
                output([make_error(f"Cannot parse time: {time_str}")])
            hour, minute = parsed
            base_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            base_dt = base_dt.replace(tzinfo=local_tz)
        else:
            base_dt = now

        utc_dt = base_dt.astimezone(timezone.utc)
        items.append(make_item(
            f"{_fmt(base_dt)} {base_dt.strftime('%Z')}",
            f"Local ({_offset_label(base_dt)})  ·  {_fmt(utc_dt)} UTC",
            arg=f"{_fmt(base_dt)} {base_dt.strftime('%Z')}",
        ))

    # Favorites
    # For ref_tz cases (ct 10am utc+7, ct utc+3): show local time → fav tz time
    # For plain cases (ct, ct 10am): show base time → fav tz time
    local_base = now if not time_str else base_dt
    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue

        tz = ZoneInfo(iana)
        target_dt = base_dt.astimezone(tz)
        date_note = format_date_diff(base_dt, target_dt)
        diff = _diff_label(base_dt, target_dt)

        if ref_tz:
            # Show "local time in that tz" → "converted time in that tz"
            # base_dt is the ref_tz time, show what it equals in this fav tz
            local_in_fav = local_base.astimezone(tz)
            items.append(make_item(
                f"{_fmt(local_in_fav)} {local_in_fav.strftime('%Z')}  →  {_fmt(target_dt)} {target_dt.strftime('%Z')}{date_note}",
                f"{loc['city']}, {loc['country']}  ·  {_offset_label(target_dt)}  ·  {diff}",
                arg=f"{_fmt(target_dt)} {target_dt.strftime('%Z')}",
            ))
        else:
            items.append(make_item(
                f"{_fmt(target_dt)} {target_dt.strftime('%Z')}{date_note}",
                f"{loc['city']}, {loc['country']}  ·  {_offset_label(target_dt)}  ·  {diff}",
                arg=f"{_fmt(target_dt)} {target_dt.strftime('%Z')}",
            ))

    output(items)


def show_time_arithmetic(time_str, offset_str):
    """Handle 'ct 10am -7', 'ct +3', 'ct -1' — time arithmetic.

    If time_str is None, use current time.
    """
    local_tz = get_local_tz()
    now = datetime.now(tz=local_tz)

    if time_str:
        parsed = parse_time(time_str)
        if not parsed:
            output([make_error(f"Cannot parse time: {time_str}")])
        hour, minute = parsed
        source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    else:
        source_dt = now

    result = resolve_bare_offset(offset_str)
    if not result:
        output([make_error(f"Cannot parse offset: {offset_str}")])

    td, label = result
    target_dt = source_dt + td
    date_note = format_date_diff(source_dt, target_dt)

    source_tz_name = source_dt.strftime("%Z")

    # Header: base (left) → result (right)
    items = [make_item(
        f"{_fmt(source_dt)} {source_tz_name}  →  {_fmt(target_dt)} {source_tz_name}{date_note}",
        f"Local ({label}){date_note}",
        arg=f"{_fmt(target_dt)}",
    )]

    # Favorites: show original time → shifted time in each tz
    favs = favorites.load()
    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue
        tz = ZoneInfo(iana)
        # Original time in this tz
        orig_fav_dt = source_dt.astimezone(tz)
        # Shifted time in this tz
        shifted_fav_dt = target_dt.astimezone(tz)
        fav_date = format_date_diff(orig_fav_dt, shifted_fav_dt)

        items.append(make_item(
            f"{_fmt(orig_fav_dt)} {orig_fav_dt.strftime('%Z')}  →  {_fmt(shifted_fav_dt)} {shifted_fav_dt.strftime('%Z')}{fav_date}",
            f"{loc['city']}, {loc['country']}  ·  {_offset_label(shifted_fav_dt)}",
            arg=f"{_fmt(shifted_fav_dt)} {shifted_fav_dt.strftime('%Z')}",
        ))

    output(items)


def handle_add(search_query):
    if not search_query:
        output([make_item(
            "Search for a city, country, or timezone",
            "e.g., ct add tokyo  |  ct add pdt  |  ct add korea",
            valid=False
        )])

    results = search_locations(search_query)
    current_favs = set(favorites.load())

    if not results:
        output([make_error(f"No results for '{search_query}'")])

    items = []
    for loc in results:
        iana = loc["iana"]
        already = iana in current_favs
        tz_abbrs = "/".join(loc["tz_abbrs"])
        title = f"{loc['city']}, {loc['country']} ({tz_abbrs})"
        if already:
            items.append(make_item(title, "Already added", arg=f"__noop__{iana}", valid=False))
        else:
            items.append(make_item(title, f"{loc['region']}  ·  {iana}  — Press Enter to add", arg=f"__add__{iana}"))

    output(items)


def handle_remove(search_query):
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
        items.append(make_item(
            f"{loc['city']}, {loc['country']} ({tz_abbrs})",
            "Press Enter to remove",
            arg=f"__remove__{iana}",
        ))

    if not items:
        output([make_error("No matching timezone found")])
    output(items)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    query = query.strip()

    # ct → dashboard
    if not query:
        show_dashboard()

    lower = query.lower()

    # ct add / ct remove
    if lower.startswith("add"):
        handle_add(query[3:].strip())
    if lower.startswith("remove") or lower.startswith("rm"):
        search = re.sub(r'^(remove|rm)\s*', '', query, flags=re.IGNORECASE).strip()
        handle_remove(search)

    # ct 12pm to pdt / ct 12pm to utc+9 → single conversion
    if " to " in lower or " in " in lower:
        parsed = parse(query)
        if isinstance(parsed, TimezoneQuery):
            items = tz_convert(parsed.time_str, parsed.to_tz, parsed.from_tz)
            output(items)

    parts = query.split()

    # ct +1 / ct -3 → current time arithmetic (bare offset, no time)
    if len(parts) == 1 and BARE_OFFSET_RE.match(parts[0]):
        show_time_arithmetic(None, parts[0])

    # ct utc / ct utc+3 / ct gmt-6 → show local → that tz
    if len(parts) == 1 and OFFSET_RE.match(parts[0]):
        result = resolve_offset_tz(parts[0])
        if result:
            ref_tz, ref_label = result
            show_dashboard(ref_tz=ref_tz, ref_label=ref_label)

    if len(parts) >= 2:
        time_part = parts[0]
        modifier = " ".join(parts[1:])

        if TIME_RE.match(time_part):
            # ct 10am -7 / ct 10am +3:30 → time arithmetic
            if BARE_OFFSET_RE.match(modifier):
                show_time_arithmetic(time_part, modifier)

            # ct 10am utc+7 / ct 10am gmt+1 → time at that tz
            if OFFSET_RE.match(modifier):
                result = resolve_offset_tz(modifier)
                if result:
                    ref_tz, ref_label = result
                    show_dashboard(time_part, ref_tz=ref_tz, ref_label=ref_label)

            # ct 10am pdt / ct 10am tokyo → time at that tz
            tz, label = resolve_tz(modifier)
            if tz:
                show_dashboard(time_part, ref_tz=tz, ref_label=label or modifier.upper())

    # ct 10am → dashboard with time
    if TIME_RE.match(query):
        show_dashboard(query)

    # Fallback
    output([make_item(
        "ct — Timezone",
        "ct | ct +1 | ct 10am | ct utc+7 | ct 10am -7 | ct 12pm to pdt",
        valid=False
    )])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        output([make_error(f"Error: {str(e)}")])
