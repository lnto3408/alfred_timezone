#!/usr/bin/env python3
"""Alfred Script Filter: Universal Converter (Timezone + Currency)."""
import os
import sys

# Ensure the script's directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converter.parser import parse, TimezoneQuery, CurrencyQuery
from converter.timezone import convert as tz_convert
from converter.currency import convert as curr_convert
from converter.alfred import output, make_item, make_error


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    query = query.strip()

    if not query:
        output([])

    # No "to"/"in" keyword yet — not a conversion query, skip silently
    if " to " not in query.lower() and " in " not in query.lower():
        output([])

    parsed = parse(query)

    if parsed is None:
        # Doesn't match our patterns — don't show anything
        output([])

    if isinstance(parsed, TimezoneQuery):
        items = tz_convert(parsed.time_str, parsed.to_tz, parsed.from_tz)
    elif isinstance(parsed, CurrencyQuery):
        items = curr_convert(parsed.amount, parsed.from_curr, parsed.to_curr)
    else:
        items = [make_error("Unknown conversion type")]

    output(items)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        output([make_error(f"Error: {str(e)}")])
