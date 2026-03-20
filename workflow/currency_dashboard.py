#!/usr/bin/env python3
"""Alfred Script Filter: cc — currency conversion + dashboard."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converter.alfred import output, make_item, make_error
from converter.data import resolve_location, search_locations, CURRENCIES, _IDX, ZERO_DECIMAL_CURRENCIES, country_flag, currency_flag
from converter import favorites
from converter.currency import get_rates, format_amount, convert as curr_convert
from converter.parser import parse, CurrencyQuery


def _get_local_currency():
    """Get local currency based on system timezone."""
    try:
        link = os.readlink("/etc/localtime")
        parts = link.split("/zoneinfo/")
        if len(parts) == 2:
            loc = _IDX["iana"].get(parts[1])
            if loc:
                return loc["currency"]
    except OSError:
        pass
    return "USD"


def _currency_name(code):
    """Get display name for a currency code."""
    for c in CURRENCIES:
        if c["code"] == code:
            return f"{c['symbol']} {c['name']}"
    return code


def show_rates(amount_str=None):
    """Show exchange rates for all favorite currencies."""
    favs = favorites.load_currencies()

    if not favs:
        output([make_item(
            "No currencies added yet",
            "Type 'cc add usd' to add a currency",
            valid=False
        )])

    local_curr = _get_local_currency()

    if amount_str:
        try:
            amount = float(amount_str.replace(",", ""))
        except ValueError:
            output([make_error(f"Invalid amount: {amount_str}")])
    else:
        high_unit = {"KRW", "JPY", "VND", "IDR", "CLP", "COP", "HUF"}
        amount = 10000.0 if local_curr in high_unit else 100.0

    rates, is_stale = get_rates(local_curr)
    if rates is None:
        output([make_error("Failed to fetch exchange rates", "Check your internet connection")])

    items = []
    amount_formatted = format_amount(amount, local_curr)
    stale_note = "  (cached)" if is_stale else ""

    items.append(make_item(
        f"{amount_formatted} {local_curr}",
        f"{_currency_name(local_curr)}  (base){stale_note}",
        arg=f"{amount_formatted} {local_curr}",
    ))

    for code in favs:
        if code == local_curr:
            continue

        rate = rates.get(code)
        if rate is None:
            continue

        result = amount * rate
        result_formatted = format_amount(result, code)

        flag = currency_flag(code)
        title = f"{flag}  {result_formatted} {code}"
        rate_str = f"{rate:.6g}" if rate < 1 else format_amount(rate, code)
        subtitle = f"{_currency_name(code)}  ·  1 {local_curr} = {rate_str} {code}"

        items.append(make_item(title, subtitle, arg=result_formatted))

    output(items)


def handle_add(search_query):
    """Search and show currencies to add."""
    if not search_query:
        output([make_item(
            "Search for a currency",
            "e.g., cc add usd  |  cc add yen  |  cc add euro",
            valid=False
        )])

    current_favs = set(favorites.load_currencies())
    query_lower = search_query.lower()
    query_upper = search_query.upper()

    items = []
    seen = set()

    for curr in CURRENCIES:
        code = curr["code"]
        if code in seen:
            continue

        match = False
        if query_upper == code:
            match = True
        elif query_lower in curr["name"].lower():
            match = True
        else:
            for alias in curr.get("aliases", []):
                if query_lower in alias.lower():
                    match = True
                    break

        if not match:
            loc = _IDX["currency"].get(code)
            if loc:
                searchable = f"{loc['city']} {loc['country']} {' '.join(loc.get('aliases', []))}".lower()
                if query_lower in searchable:
                    match = True

        if match:
            seen.add(code)
            already = code in current_favs
            title = f"{curr['symbol']}  {code} — {curr['name']}"

            if already:
                items.append(make_item(title, "✓ Already added", arg=f"__noop__{code}", valid=False))
            else:
                loc = _IDX["currency"].get(code)
                region = f"{loc['city']}, {loc['country']}" if loc else ""
                subtitle = f"{region}  — Press Enter to add" if region else "Press Enter to add"
                items.append(make_item(title, subtitle, arg=f"__add__{code}"))

    if not items:
        output([make_error(f"No currency found for '{search_query}'")])

    output(items[:15])


def handle_remove(search_query):
    """Show current favorite currencies for removal."""
    favs = favorites.load_currencies()
    if not favs:
        output([make_item("No currencies to remove", "Add some first with 'cc add'", valid=False)])

    items = []
    for code in favs:
        name = _currency_name(code)
        if search_query and search_query.upper() not in code and search_query.lower() not in name.lower():
            continue
        title = f"{code} — {name}"
        items.append(make_item(title, "Press Enter to remove", arg=f"__remove__{code}"))

    if not items:
        output([make_error("No matching currency found")])

    output(items)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    query = query.strip()

    # cc → dashboard (default amount)
    if not query:
        show_rates()

    lower = query.lower()

    # cc add <search>
    if lower.startswith("add"):
        handle_add(query[3:].strip())

    # cc remove / cc rm
    if lower.startswith("remove") or lower.startswith("rm"):
        search = re.sub(r'^(remove|rm)\s*', '', query, flags=re.IGNORECASE).strip()
        handle_remove(search)

    # cc 1000 krw to usd → single conversion
    if " to " in lower or " in " in lower:
        parsed = parse(query)
        if isinstance(parsed, CurrencyQuery):
            items = curr_convert(parsed.amount, parsed.from_curr, parsed.to_curr)
            output(items)

    # cc 1000 → dashboard with amount
    amount_match = re.match(r'^[\d,]+\.?\d*$', query)
    if amount_match:
        show_rates(query)

    # Fallback
    output([make_item(
        "cc — Currency",
        "cc [amount] | cc 1000 krw to usd | cc add [currency] | cc remove [name]",
        valid=False
    )])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        output([make_error(f"Error: {str(e)}")])
