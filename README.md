# Universal Converter for Alfred

Raycast-style inline converter for Alfred. No keyword needed — just type directly in Alfred's search bar and get instant results.

![timezone](https://img.shields.io/badge/timezone-DST%20aware-blue)
![currency](https://img.shields.io/badge/currency-160%2B%20codes-green)
![python](https://img.shields.io/badge/python-3.9%2B%20stdlib-yellow)

## Features

- **No keyword prefix** — results appear inline alongside Alfred's default results
- **Timezone conversion** with automatic DST handling
- **Currency conversion** with real-time exchange rates (cached 1 hour)
- **Zero dependencies** — Python 3.9+ standard library only, no `pip install` needed
- **Clipboard copy** — press Enter to copy the result

## Install

Download the latest `.alfredworkflow` from [Releases](https://github.com/lnto3408/alfred_timezone/releases), then double-click to install.

Or build from source:

```bash
chmod +x build.sh
./build.sh
# double-click Universal-Converter.alfredworkflow
```

## Usage

### Timezone

Type directly in Alfred:

| Input | Output |
|---|---|
| `12pm to pdt` | 8:00 PM PDT (previous day) |
| `3:30pm to est` | 2:30 AM EDT |
| `9am kst to pdt` | 5:00 PM PDT (previous day) |
| `15:00 to tokyo` | 3:00 PM JST |
| `12pm to utc` | 3:00 AM UTC |

- Source timezone defaults to your system's local timezone if omitted
- Supports abbreviations: `PST`, `PDT`, `EST`, `EDT`, `CST`, `CDT`, `JST`, `KST`, `GMT`, `UTC`, `CET`, `IST`, `AEST`, etc.
- Supports city names: `tokyo`, `london`, `nyc`, `sf`, `seoul`, `sydney`, `paris`, `dubai`, etc.
- Time formats: `12pm`, `3:30pm`, `15:00`, `0930`

### Currency

| Input | Output |
|---|---|
| `1000 krw to usd` | 0.67 USD |
| `50 eur to jpy` | 9,135 JPY |
| `100 usd to gbp` | 79.42 GBP |

- 160+ currency codes supported (ISO 4217)
- Exchange rates from [open.er-api.com](https://open.er-api.com) — free, no API key
- Rates cached locally for 1 hour at `~/.cache/alfred_converter/`
- Stale cache used as fallback when offline

## How it works

This workflow uses Alfred's **Script Filter** with an empty keyword, so it runs on every query. When the input doesn't match a conversion pattern (e.g. `<time> to <timezone>` or `<amount> <currency> to <currency>`), it returns empty results and doesn't interfere with other workflows or Alfred's default search.

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
