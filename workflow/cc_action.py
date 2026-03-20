#!/usr/bin/env python3
"""Handle cc add/remove actions from Alfred."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converter import favorites

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg.startswith("__add__"):
        code = arg[7:]
        if favorites.add_currency(code):
            print(f"Added {code}")
        else:
            print(f"{code} already in favorites")

    elif arg.startswith("__remove__"):
        code = arg[10:]
        if favorites.remove_currency(code):
            print(f"Removed {code}")
        else:
            print(f"{code} not in favorites")

if __name__ == "__main__":
    main()
