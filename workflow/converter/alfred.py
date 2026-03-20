"""Alfred Script Filter JSON output helpers."""
import json
import sys


def make_item(title, subtitle="", arg=None, icon=None, valid=True):
    item = {
        "title": title,
        "subtitle": subtitle,
        "arg": arg or title,
        "valid": valid,
    }
    if icon:
        item["icon"] = {"path": icon}
    return item


def make_error(message, subtitle=""):
    return make_item(message, subtitle=subtitle, valid=False)


def output(items):
    result = {"items": items if items else []}
    print(json.dumps(result))
    sys.exit(0)
