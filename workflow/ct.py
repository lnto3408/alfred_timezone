#!/usr/bin/env python3
"""Alfred Script Filter: ct — timezone dashboard with favorites."""
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converter.alfred import output, make_item, make_error
from converter.data import resolve_location, search_locations, format_location, LOCATIONS, _IDX
from converter import favorites
from converter.timezone import parse_time, get_local_tz


def show_times(time_str=None):
    """Show time across all favorite timezones."""
    favs = favorites.load()

    if not favs:
        output([make_item(
            "No timezones added yet",
            "Type 'ct add tokyo' to add a timezone",
            valid=False
        )])

    local_tz = get_local_tz()
    now = datetime.now(tz=local_tz)

    if time_str:
        parsed = parse_time(time_str)
        if not parsed:
            output([make_error(f"Cannot parse time: {time_str}", "Try: 10am, 3:30pm, 15:00")])
        hour, minute = parsed
        source_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    else:
        source_dt = now

    items = []
    source_tz_name = source_dt.strftime("%Z")
    source_fmt = source_dt.strftime("%-I:%M %p")

    # Header: local time
    items.append(make_item(
        f"🏠 {source_fmt} {source_tz_name} (Local)",
        f"Your local time",
        arg=f"{source_fmt} {source_tz_name}",
    ))

    for iana in favs:
        loc = _IDX["iana"].get(iana)
        if not loc:
            continue

        tz = ZoneInfo(iana)
        target_dt = source_dt.astimezone(tz)
        target_fmt = target_dt.strftime("%-I:%M %p")
        target_tz_name = target_dt.strftime("%Z")

        # Date difference
        date_note = ""
        if source_dt.date() != target_dt.date():
            diff = (target_dt.date() - source_dt.date()).days
            if diff == 1:
                date_note = " +1d"
            elif diff == -1:
                date_note = " -1d"
            else:
                date_note = f" ({target_dt.strftime('%b %-d')})"

        title = f"{target_fmt} {target_tz_name}{date_note}"
        subtitle = f"{loc['city']}, {loc['country']}  ·  {target_tz_name} (UTC{target_dt.strftime('%z')[:3]})"

        items.append(make_item(title, subtitle, arg=f"{target_fmt} {target_tz_name}"))

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
            subtitle = "✓ Already added"
            items.append(make_item(title, subtitle, arg=f"__noop__{iana}", valid=False))
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
        subtitle = f"Press Enter to remove"
        items.append(make_item(title, subtitle, arg=f"__remove__{iana}"))

    if not items:
        output([make_error(f"No matching timezone found", "Check your favorites")])

    output(items)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    query = query.strip()

    # ct (no args) → show current time in all favorites
    if not query:
        show_times()

    lower = query.lower()

    # ct add <search>
    if lower.startswith("add"):
        search = query[3:].strip()
        handle_add(search)

    # ct remove <search> / ct rm <search>
    if lower.startswith("remove") or lower.startswith("rm"):
        search = re.sub(r'^(remove|rm)\s*', '', query, flags=re.IGNORECASE).strip()
        handle_remove(search)

    # ct <time> → show time in all favorites
    # Check if query looks like a time
    time_match = re.match(r'^(\d{1,2}(?::\d{2})?\s*(?:am|pm)|\d{1,2}:\d{2}|\d{4})\s*$', query, re.IGNORECASE)
    if time_match:
        show_times(time_match.group(1))

    # Fallback: try as time anyway, or show help
    output([make_item(
        "ct — Timezone Dashboard",
        "ct [time] | ct add [city/country/tz] | ct remove [name]",
        valid=False
    )])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        output([make_error(f"Error: {str(e)}")])
