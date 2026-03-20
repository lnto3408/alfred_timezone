#!/usr/bin/env python3
"""Handle ct add/remove actions from Alfred."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converter import favorites

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg.startswith("__add__"):
        iana = arg[7:]
        if favorites.add(iana):
            print(f"Added {iana}")
        else:
            print(f"{iana} already in favorites")

    elif arg.startswith("__remove__"):
        iana = arg[10:]
        if favorites.remove(iana):
            print(f"Removed {iana}")
        else:
            print(f"{iana} not in favorites")

if __name__ == "__main__":
    main()
