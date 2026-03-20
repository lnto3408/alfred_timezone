# Universal Converter for Alfred

Timezone and currency converter for Alfred — dashboard, conversion, and favorites management from the search bar.

![timezone](https://img.shields.io/badge/timezone-DST%20aware-blue)
![currency](https://img.shields.io/badge/currency-160%2B%20codes-green)
![python](https://img.shields.io/badge/python-3.9%2B%20stdlib-yellow)

## Requirements

- macOS with Python 3.9+ (pre-installed on macOS)
- [Alfred](https://www.alfredapp.com/) with Powerpack
- No `pip install` needed — uses Python standard library only

## Install

Download `Universal-Converter.alfredworkflow` from [Releases](https://github.com/lnto3408/alfred_timezone/releases) and double-click to install.

Or build from source:

```bash
chmod +x build.sh
./build.sh
# double-click Universal-Converter.alfredworkflow
```

## Usage

Two keywords: **`ct`** for timezone, **`cc`** for currency.

> **Tip:** Keywords can be changed — see [Customizing keywords](#customizing-keywords).

---

### `ct` — Timezone

Dashboard + conversion + favorites, all in one.

| Input | Result |
|---|---|
| `ct` | Current time in all saved timezones |
| `ct 10am` | 10:00 AM (local) → all saved timezones |
| `ct 12pm to pdt` | Single conversion: 12:00 PM local → PDT |
| `ct 3:30pm kst to est` | Single conversion with source timezone |
| `ct 15:00 to tokyo` | City name as target |
| `ct add tokyo` | Add timezone by city/country/abbreviation |
| `ct add pdt` | Add by timezone abbreviation |
| `ct add korea` | Add by country |
| `ct remove tokyo` | Remove timezone |
| `ct rm london` | Remove (short form) |

Saved timezones: `~/.config/alfred_converter/favorites.json`

---

### `cc` — Currency

Dashboard + conversion + favorites, all in one.

| Input | Result |
|---|---|
| `cc` | Default amount → all saved currencies |
| `cc 5000` | 5,000 local currency → all saved currencies |
| `cc 1000 krw to usd` | Single conversion: 1,000 KRW → USD |
| `cc 50 eur to jpy` | Single conversion: 50 EUR → JPY |
| `cc add usd` | Add currency by code |
| `cc add yen` | Add by alias |
| `cc add euro` | Add by name |
| `cc remove jpy` | Remove currency |
| `cc rm eur` | Remove (short form) |

Local currency auto-detected from system timezone. Saved currencies: `~/.config/alfred_converter/currencies.json`

---

### Supported formats

#### Timezone identifiers

| Type | Examples |
|---|---|
| Abbreviation | `PST`, `PDT`, `PT`, `EST`, `EDT`, `ET`, `CST`, `CDT`, `CT`, `MST`, `MDT`, `MT`, `JST`, `KST`, `GMT`, `BST`, `CET`, `CEST`, `EET`, `IST`, `AEST`, `AEDT`, `NZST`, `NZDT`, `HST`, `UTC` |
| City | `tokyo`, `london`, `nyc`, `sf`, `seoul`, `sydney`, `paris`, `berlin`, `dubai`, `singapore`, `mumbai`, `toronto` |
| Country / Region | `japan`, `korea`, `uk`, `france`, `germany`, `australia`, `brazil`, `india`, `thailand` |
| Alias | `la`, `hk`, `dc`, `west coast`, `east coast`, `hawaii` |
| IANA | `America/New_York`, `Asia/Seoul`, `Europe/London` |

#### Time formats

| Format | Example |
|---|---|
| 12-hour | `12pm`, `3:30pm`, `9am` |
| 24-hour | `15:00`, `9:30` |
| 4-digit | `1430`, `0900` |

#### Currency codes

Standard 3-letter ISO 4217 codes: `USD`, `EUR`, `GBP`, `JPY`, `KRW`, `CNY`, `CAD`, `AUD`, `CHF`, `SGD`, `HKD`, `TWD`, `THB`, `INR`, `BRL`, `MXN`, `ZAR`, `AED`, `SEK`, `NOK`, `DKK`, `PLN`, `CZK`, `TRY`, `RUB`, and [160+ more](https://open.er-api.com/v6/latest/USD).

Exchange rates from [open.er-api.com](https://open.er-api.com) — free, no API key. Cached 1 hour at `~/.cache/alfred_converter/`.

## Customizing keywords

1. Open **Alfred Preferences** → **Workflows**
2. Select **Universal Converter**
3. Double-click the **Script Filter** block you want to change (`ct` or `cc`)
4. Edit the **Keyword** field
5. Close — changes are saved automatically

## Project structure

```
├── workflow/
│   ├── info.plist              # Alfred workflow manifest
│   ├── icon.png                # Workflow icon
│   ├── timezone_dashboard.py   # 'ct' — timezone dashboard + conversion
│   ├── timezone_action.py      # ct add/remove handler
│   ├── currency_dashboard.py   # 'cc' — currency dashboard + conversion
│   ├── currency_action.py      # cc add/remove handler
│   └── converter/
│       ├── data.py             # Timezone/city/country/currency data table
│       ├── alfred.py           # Alfred JSON output helpers
│       ├── parser.py           # Query parsing & routing
│       ├── timezone.py         # Timezone conversion (zoneinfo)
│       ├── currency.py         # Currency conversion + caching
│       └── favorites.py        # Saved timezone/currency management
├── build.sh
├── LICENSE
└── README.md
```

## License

MIT
