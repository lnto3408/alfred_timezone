# Universal Converter for Alfred

Instant timezone & currency converter for Alfred. Type `c` followed by your query and get real-time results as you type.

![timezone](https://img.shields.io/badge/timezone-DST%20aware-blue)
![currency](https://img.shields.io/badge/currency-160%2B%20codes-green)
![python](https://img.shields.io/badge/python-3.9%2B%20stdlib-yellow)

## Features

- **Timezone conversion** with automatic DST handling
- **Currency conversion** with real-time exchange rates (cached 1 hour)
- **Instant results** — no Enter needed, results update as you type
- **Zero dependencies** — Python 3.9+ standard library only, no `pip install`
- **Clipboard copy** — press Enter to copy the result

## Install

Download `Universal-Converter.alfredworkflow` from [Releases](https://github.com/lnto3408/alfred_timezone/releases) and double-click to install.

Or build from source:

```bash
chmod +x build.sh
./build.sh
# double-click Universal-Converter.alfredworkflow
```

## Usage

Open Alfred and type `c` followed by a space, then your conversion query.

> **Tip:** The keyword `c` is just the default. You can change it to anything you like — see [Changing the keyword](#changing-the-keyword) below.

### Timezone

| Input | Output |
|---|---|
| `c 12pm to pdt` | 8:00 PM PDT (previous day) |
| `c 3:30pm to est` | 2:30 AM EDT |
| `c 9am kst to pdt` | 5:00 PM PDT (previous day) |
| `c 15:00 to tokyo` | 3:00 PM JST |
| `c 12pm to utc` | 3:00 AM UTC |

- Source timezone defaults to your **system's local timezone** if omitted
- Supports abbreviations: `PST`, `PDT`, `EST`, `EDT`, `CST`, `CDT`, `JST`, `KST`, `GMT`, `UTC`, `CET`, `IST`, `AEST`, etc.
- Supports city names: `tokyo`, `london`, `nyc`, `sf`, `seoul`, `sydney`, `paris`, `dubai`, etc.
- Time formats: `12pm`, `3:30pm`, `15:00`, `0930`

### Currency

| Input | Output |
|---|---|
| `c 1000 krw to usd` | 0.67 USD |
| `c 50 eur to jpy` | 9,135 JPY |
| `c 100 usd to gbp` | 79.42 GBP |

- 160+ currency codes supported (ISO 4217)
- Exchange rates from [open.er-api.com](https://open.er-api.com) — free, no API key needed
- Rates cached locally for 1 hour at `~/.cache/alfred_converter/`
- Stale cache used as fallback when offline

## Changing the keyword

1. Open **Alfred Preferences** → **Workflows**
2. Select **Universal Converter**
3. Double-click the **Script Filter** block (the leftmost block)
4. Change the **Keyword** field to whatever you prefer (e.g., `cv`, `=`, `conv`)
5. Close the dialog — changes are saved automatically

## Project structure

```
├── workflow/              # Alfred workflow source
│   ├── info.plist         # Alfred workflow manifest
│   ├── main.py            # Entry point (Script Filter)
│   └── converter/
│       ├── alfred.py      # Alfred JSON output helpers
│       ├── parser.py      # Query parsing & routing
│       ├── timezone.py    # Timezone conversion (zoneinfo)
│       └── currency.py    # Currency conversion + caching
├── build.sh               # Package into .alfredworkflow
├── LICENSE
└── README.md
```

## Requirements

- macOS with Python 3.9+ (pre-installed on macOS)
- [Alfred](https://www.alfredapp.com/) with Powerpack

## License

MIT
