# Universal Converter for Alfred

Timezone dashboard & instant converter for Alfred — timezone conversion, currency conversion, and a multi-timezone clock, all from the Alfred search bar.

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

Three keywords: **`c`** for quick conversions, **`ct`** for the timezone dashboard, **`cc`** for the currency dashboard.

> **Tip:** Both keywords can be changed to anything you prefer — see [Customizing keywords](#customizing-keywords).

---

### `c` — Convert

Quick timezone and currency conversions.

#### Timezone

| Input | Output |
|---|---|
| `c 12pm to pdt` | 8:00 PM PDT (previous day) |
| `c 3:30pm to est` | 2:30 AM EDT |
| `c 9am kst to pdt` | 5:00 PM PDT (previous day) |
| `c 15:00 to tokyo` | 3:00 PM JST |
| `c 12pm to utc` | 3:00 AM UTC |

- Source timezone defaults to your **system's local timezone** when omitted
- Shows date context when day changes (e.g., "previous day", "next day")
- Time formats: `12pm`, `3:30pm`, `15:00`, `0930`

#### Currency

| Input | Output |
|---|---|
| `c 1000 krw to usd` | 0.67 USD |
| `c 50 eur to jpy` | 9,135 JPY |
| `c 100 usd to gbp` | 79.42 GBP |

- 160+ currency codes (ISO 4217)
- Exchange rates from [open.er-api.com](https://open.er-api.com) — free, no API key
- Rates cached for 1 hour at `~/.cache/alfred_converter/`
- Stale cache used as fallback when offline

**Press Enter** to copy the result to clipboard.

---

### `ct` — Timezone Dashboard

Save your frequently-used timezones and see them all at a glance.

#### View current time across saved timezones

| Input | Result |
|---|---|
| `ct` | Current time in all saved timezones |
| `ct 10am` | 10:00 AM (local) converted to all saved timezones |
| `ct 3:30pm` | 3:30 PM (local) converted to all saved timezones |

#### Add / remove timezones

| Input | Result |
|---|---|
| `ct add tokyo` | Search & add Tokyo (JST) |
| `ct add pdt` | Search & add by timezone abbreviation |
| `ct add korea` | Search & add by country name |
| `ct remove tokyo` | Remove Tokyo from dashboard |
| `ct rm london` | Remove London from dashboard |

Saved timezones are stored at `~/.config/alfred_converter/favorites.json`.

---

### `cc` — Currency Dashboard

Save your frequently-used currencies and compare rates at a glance.

#### View rates for saved currencies

| Input | Result |
|---|---|
| `cc` | 1 unit of local currency → all saved currencies |
| `cc 1000` | 1,000 local currency → all saved currencies |
| `cc 50000` | 50,000 local currency → all saved currencies |

Your **local currency is auto-detected** from your system timezone (e.g., KRW for Asia/Seoul).

#### Add / remove currencies

| Input | Result |
|---|---|
| `cc add usd` | Add US Dollar |
| `cc add yen` | Search by alias → add JPY |
| `cc add euro` | Search by name → add EUR |
| `cc remove jpy` | Remove Japanese Yen |
| `cc rm eur` | Remove Euro |

Saved currencies are stored at `~/.config/alfred_converter/currencies.json`.

---

### Supported formats

#### Timezone identifiers

You can use any of the following to specify a timezone:

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

## Customizing keywords

1. Open **Alfred Preferences** → **Workflows**
2. Select **Universal Converter**
3. Double-click the **Script Filter** block you want to change (`c`, `ct`, or `cc`)
4. Edit the **Keyword** field (e.g., change `c` to `conv`, `ct` to `tz`, `cc` to `cur`)
5. Close — changes are saved automatically

## Project structure

```
├── workflow/               # Alfred workflow source
│   ├── info.plist          # Alfred workflow manifest
│   ├── main.py             # 'c' keyword — convert entry point
│   ├── ct.py               # 'ct' keyword — timezone dashboard
│   ├── ct_action.py        # Add/remove timezone action handler
│   ├── cc.py               # 'cc' keyword — currency dashboard
│   ├── cc_action.py        # Add/remove currency action handler
│   └── converter/
│       ├── data.py         # Timezone/city/country/currency data table
│       ├── alfred.py       # Alfred JSON output helpers
│       ├── parser.py       # Query parsing & routing
│       ├── timezone.py     # Timezone conversion (zoneinfo)
│       ├── currency.py     # Currency conversion + caching
│       └── favorites.py    # Saved timezone management
├── build.sh                # Package into .alfredworkflow
├── LICENSE
└── README.md
```

## License

MIT
