#!/usr/bin/env python3
"""Alfred Script Filter: ct — timezone conversion + dashboard.

Supports:
  ct                     → dashboard (current time in favorites)
  ct 10am                → dashboard with specific time
  ct +1 / ct -3          → current time +/- hours (arithmetic)
  ct 10am -7             → 10am minus 7 hours
  ct utc+3 / ct gmt-6    → show local → that tz + favorites
  ct 10am utc+7          → 10am at UTC+7, show as local + favorites
  ct 12pm to pdt         → single conversion
  ct add tokyo           → add to favorites
  ct remove tokyo        → remove from favorites
  ct format              → choose clipboard time format
"""
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converter.alfred import output, make_item, make_error
from converter.data import resolve_location, search_locations, LOCATIONS, _IDX, country_flag
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
    off = dt.utcoffset()
    if off is None:
        return ""
    return "UTC" + format_offset(off)


def _diff_label(source_dt, target_dt):
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
    return dt.strftime("%-I:%M %p")


def _copy_fmt(dt):
    """Format for clipboard using user's chosen format."""
    fmt = favorites.get_time_format()
    return dt.strftime(fmt)


def _flag(loc):
    """Get flag emoji for a location."""
    if not loc:
        return ""
    return country_flag(loc.get("cc", ""))


def _loc_sub(loc, dt):
    """Subtitle: city, country, offset."""
    return f"{loc['city']}, {loc['country']}  ·  {_offset_label(dt)}"


def _loc_sub_diff(loc, dt, base_dt):
    """Subtitle: city, country, offset, diff."""
    diff = _diff_label(base_dt, dt)
    return f"{loc['city']}, {loc['country']}  ·  {_offset_label(dt)}  ·  {diff}"


def show_dashboard(time_str=None, ref_tz=None, ref_label=None, source_datetime=None):
    """Show timezone dashboard.

    Args:
        time_str: simple time like '10am'
        ref_tz: reference timezone for the time
        ref_label: display label for ref_tz
        source_datetime: a full datetime object (from log timestamps)
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

    # Full datetime from log timestamp
    if source_datetime:
        base_dt = source_datetime
        local_dt = base_dt.astimezone(local_tz)
        src_tz_label = base_dt.strftime("%Z") or _offset_label(base_dt)

        items.append(make_item(
            f"{base_dt.strftime('%Y-%m-%d %-I:%M %p')} {src_tz_label}  →  {_fmt(local_dt)} {local_dt.strftime('%Z')}",
            f"Parsed timestamp → Local ({_offset_label(local_dt)})",
            arg=_copy_fmt(local_dt),
        ))

        for iana in favs:
            loc = _IDX["iana"].get(iana)
            if not loc:
                continue
            tz = ZoneInfo(iana)
            target_dt = base_dt.astimezone(tz)
            date_note = format_date_diff(base_dt, target_dt)
            items.append(make_item(
                f"{_flag(loc)}  {_fmt(target_dt)} {target_dt.strftime('%Z')}  ({target_dt.strftime('%b %-d')}){date_note}",
                _loc_sub_diff(loc, target_dt, local_dt),
                arg=_copy_fmt(target_dt),
            ))

        output(items)

    if ref_tz and time_str:
        parsed = parse_time(time_str)
        if not parsed:
            output([make_error(f"Cannot parse time: {time_str}")])
        hour, minute = parsed
        source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        source_dt = source_dt.replace(tzinfo=ref_tz)
        local_dt = source_dt.astimezone(local_tz)
        date_note = format_date_diff(source_dt, local_dt)

        items.append(make_item(
            f"{_fmt(source_dt)} {ref_label}  →  {_fmt(local_dt)} {local_dt.strftime('%Z')}{date_note}",
            f"{ref_label} → Local ({_offset_label(local_dt)})",
            arg=_copy_fmt(local_dt),
        ))
        base_dt = source_dt

    elif ref_tz and not time_str:
        target_dt = now.astimezone(ref_tz)
        date_note = format_date_diff(now, target_dt)

        items.append(make_item(
            f"{_fmt(now)} {now.strftime('%Z')}  →  {_fmt(target_dt)} {ref_label}{date_note}",
            f"Local ({_offset_label(now)}) → {ref_label}",
            arg=_copy_fmt(target_dt),
        ))
        base_dt = now

    else:
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
            arg=_copy_fmt(base_dt),
        ))

    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue

        tz = ZoneInfo(iana)
        flag = _flag(loc)

        if ref_tz and not time_str:
            # ct utc+5: just show each tz's current time
            fav_now = now.astimezone(tz)
            diff = _diff_label(now, fav_now)
            items.append(make_item(
                f"{flag}  {_fmt(fav_now)} {fav_now.strftime('%Z')}",
                _loc_sub_diff(loc, fav_now, base_dt),
                arg=_copy_fmt(fav_now),
            ))
        elif ref_tz and time_str:
            # ct 10am utc+7: show converted time in each fav tz
            target_dt = base_dt.astimezone(tz)
            date_note = format_date_diff(base_dt, target_dt)
            items.append(make_item(
                f"{flag}  {_fmt(target_dt)} {target_dt.strftime('%Z')}{date_note}",
                _loc_sub_diff(loc, target_dt, base_dt),
                arg=_copy_fmt(target_dt),
            ))
        else:
            # ct / ct 10am: show time in each fav tz
            target_dt = base_dt.astimezone(tz)
            date_note = format_date_diff(base_dt, target_dt)
            items.append(make_item(
                f"{flag}  {_fmt(target_dt)} {target_dt.strftime('%Z')}{date_note}",
                _loc_sub_diff(loc, target_dt, base_dt),
                arg=_copy_fmt(target_dt),
            ))

    output(items)


def show_time_arithmetic(time_str, offset_str):
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

    items = [make_item(
        f"{_fmt(source_dt)} {source_tz_name}  →  {_fmt(target_dt)} {source_tz_name}{date_note}",
        f"Local ({label}){date_note}",
        arg=_copy_fmt(target_dt),
    )]

    favs = favorites.load()
    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue
        tz = ZoneInfo(iana)
        orig_fav_dt = source_dt.astimezone(tz)
        shifted_fav_dt = target_dt.astimezone(tz)
        fav_date = format_date_diff(orig_fav_dt, shifted_fav_dt)

        items.append(make_item(
            f"{_flag(loc)}  {_fmt(orig_fav_dt)} {orig_fav_dt.strftime('%Z')}  →  {_fmt(shifted_fav_dt)} {shifted_fav_dt.strftime('%Z')}{fav_date}",
            _loc_sub(loc, shifted_fav_dt),
            arg=_copy_fmt(shifted_fav_dt),
        ))

    output(items)


def handle_format(search_query):
    """Show time format options."""
    current_id = favorites.get_time_format_id()
    items = []

    for preset in favorites.TIME_FORMATS:
        is_current = preset["id"] == current_id
        marker = "  ✓" if is_current else ""
        items.append(make_item(
            f"{preset['label']}{marker}",
            f"Format: {preset['fmt']}  — Press Enter to select",
            arg=f"__format__{preset['id']}",
            valid=not is_current,
        ))

    # Custom option
    is_custom = current_id == "custom"
    custom_fmt = favorites.get_time_format() if is_custom else ""
    marker = "  ✓" if is_custom else ""
    hint = f"Current: {custom_fmt}" if is_custom else "e.g., ct format custom %Y/%m/%d %H:%M %Z"
    items.append(make_item(
        f"Custom strftime format{marker}",
        hint,
        arg="__format__custom",
        valid=False,
    ))

    # Handle "ct format custom <fmt>"
    if search_query and search_query.lower().startswith("custom"):
        custom = search_query[6:].strip()
        if custom:
            try:
                preview = datetime.now().strftime(custom)
                items = [make_item(
                    f"Preview: {preview}",
                    f"Format: {custom}  — Press Enter to set",
                    arg=f"__format_custom__{custom}",
                )]
            except Exception:
                items = [make_error(f"Invalid format: {custom}")]

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
        flag = _flag(loc)
        title = f"{flag}  {loc['city']}, {loc['country']} ({tz_abbrs})"
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
        flag = _flag(loc)
        items.append(make_item(
            f"{flag}  {loc['city']}, {loc['country']} ({tz_abbrs})",
            "Press Enter to remove",
            arg=f"__remove__{iana}",
        ))

    if not items:
        output([make_error("No matching timezone found")])
    output(items)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    query = query.strip()

    if not query:
        show_dashboard()

    lower = query.lower()

    # ct format [custom <fmt>]
    if lower.startswith("format"):
        handle_format(query[6:].strip())

    # ct add / ct remove
    if lower.startswith("add"):
        handle_add(query[3:].strip())
    if lower.startswith("remove") or lower.startswith("rm"):
        search = re.sub(r'^(remove|rm)\s*', '', query, flags=re.IGNORECASE).strip()
        handle_remove(search)

    # ct <timestamp> to pdt / ct 12pm to utc+9
    if " to " in lower or " in " in lower:
        # Try parser (handles both simple time and timestamps)
        parsed = parse(query)
        if isinstance(parsed, TimezoneQuery):
            items = tz_convert(parsed.time_str, parsed.to_tz, parsed.from_tz)
            output(items)

    parts = query.split()

    # ct +1 / ct -3
    if len(parts) == 1 and BARE_OFFSET_RE.match(parts[0]):
        show_time_arithmetic(None, parts[0])

    # ct utc / ct utc+3 / ct gmt-6
    if len(parts) == 1 and OFFSET_RE.match(parts[0]):
        result = resolve_offset_tz(parts[0])
        if result:
            ref_tz, ref_label = result
            show_dashboard(ref_tz=ref_tz, ref_label=ref_label)

    if len(parts) >= 2:
        time_part = parts[0]
        modifier = " ".join(parts[1:])

        if TIME_RE.match(time_part):
            if BARE_OFFSET_RE.match(modifier):
                show_time_arithmetic(time_part, modifier)

            if OFFSET_RE.match(modifier):
                result = resolve_offset_tz(modifier)
                if result:
                    ref_tz, ref_label = result
                    show_dashboard(time_part, ref_tz=ref_tz, ref_label=ref_label)

            tz, label = resolve_tz(modifier)
            if tz:
                show_dashboard(time_part, ref_tz=tz, ref_label=label or modifier.upper())

    if TIME_RE.match(query):
        show_dashboard(query)

    # Try parsing as full datetime/timestamp (log formats, unix timestamp, ISO)
    from converter.timezone import parse_datetime
    dt_result = parse_datetime(query)
    if dt_result:
        dt, _ = dt_result
        show_dashboard(source_datetime=dt)

    output([make_item(
        "ct — Timezone",
        "ct | ct +1 | ct 10am | ct utc+7 | ct 12pm to pdt | ct 2026-03-07T07:49:58",
        valid=False
    )])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        output([make_error(f"Error: {str(e)}")])
