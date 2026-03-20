# Universal Converter for Alfred

Timezone and currency converter for Alfred — dashboard, conversion, and favorites management from the search bar. Paste log timestamps, use UTC/GMT offsets, do time arithmetic, and see country flags at a glance.

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

Dashboard, conversion, UTC/GMT offsets, time arithmetic, log timestamps, and favorites.

#### Dashboard

| Input | Result |
|---|---|
| `ct` | Current time in all saved timezones |
| `ct 10am` | 10:00 AM (local) → all saved timezones |

#### Conversion

| Input | Result |
|---|---|
| `ct 12pm to pdt` | Single conversion: local → PDT |
| `ct 3:30pm kst to est` | With source timezone |
| `ct 15:00 to tokyo` | City name as target |
| `ct 12pm to utc+9` | Convert to UTC offset |
| `ct 12pm utc+9 to pdt` | From offset to named timezone |

#### UTC / GMT offsets

| Input | Result |
|---|---|
| `ct utc` | Current local → UTC |
| `ct utc+3` | Current local → UTC+3 |
| `ct gmt-6` | Current local → GMT-6 |
| `ct 10am utc+7` | 10am at UTC+7 → local + favorites |
| `ct 10am gmt+5:30` | Minute-level offsets (India, Nepal) |

#### Time arithmetic

| Input | Result |
|---|---|
| `ct +1` | Current time + 1 hour |
| `ct -3` | Current time - 3 hours |
| `ct 10am -7` | 10:00 AM - 7 hours = 3:00 AM |
| `ct 10am +3:30` | 10:00 AM + 3h30m = 1:30 PM |

#### Log timestamps

Paste any timestamp from logs — it will be parsed and shown in all saved timezones.

| Input | Format |
|---|---|
| `ct 2026-03-07T07:49:58.720` | ISO 8601 |
| `ct 2026-03-07T07:49:58Z` | ISO 8601 UTC |
| `ct 2026-03-07T07:49:58+09:00` | ISO 8601 with offset |
| `ct 2026-03-07 07:49:58` | Space-separated |
| `ct 1741322998` | Unix timestamp (seconds) |
| `ct 1741322998720` | Unix timestamp (milliseconds) |
| `ct 07/Mar/2026:07:49:58 +0900` | Apache/nginx log |
| `ct Mar 7, 2026 07:49:58` | Human readable |
| `ct 20260307T074958` | Compact ISO |

Timestamps with embedded timezone (`Z`, `+09:00`) use that timezone. Without timezone info, assumes local.

Single conversion also works: `ct 2026-03-07T07:49:58Z to pdt`

#### Favorites

| Input | Result |
|---|---|
| `ct add tokyo` | Add by city |
| `ct add pdt` | Add by abbreviation |
| `ct add korea` | Add by country |
| `ct remove tokyo` | Remove timezone |
| `ct rm london` | Remove (short form) |

Saved at `~/.config/alfred_converter/favorites.json`

#### Clipboard format

| Input | Result |
|---|---|
| `ct format` | Choose clipboard time format |
| `ct format custom %Y/%m/%d %H:%M %Z` | Set custom strftime format |

Presets: `3:30 PM`, `3:30 PM PST`, `15:30`, `15:30 PST`, `2026-03-20 15:30 PST`, `Mar 20, 3:30 PM PST`, ISO 8601.

Saved at `~/.config/alfred_converter/settings.json`

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

Local currency auto-detected from system timezone. Saved at `~/.config/alfred_converter/currencies.json`

---

### Supported identifiers

#### Timezone

| Type | Examples |
|---|---|
| Abbreviation | `PST`, `PDT`, `PT`, `EST`, `EDT`, `ET`, `CST`, `CDT`, `CT`, `MST`, `MDT`, `MT`, `JST`, `KST`, `GMT`, `BST`, `CET`, `CEST`, `EET`, `IST`, `AEST`, `AEDT`, `NZST`, `NZDT`, `HST`, `UTC` |
| UTC/GMT offset | `utc`, `gmt`, `utc+9`, `gmt-6`, `utc+5:30`, `gmt+5:45` |
| City | `tokyo`, `london`, `nyc`, `sf`, `seoul`, `sydney`, `paris`, `berlin`, `dubai`, `singapore`, `mumbai`, `toronto` |
| Country / Region | `japan`, `korea`, `uk`, `france`, `germany`, `australia`, `brazil`, `india`, `thailand` |
| Alias | `la`, `hk`, `dc`, `west coast`, `east coast`, `hawaii` |
| IANA | `America/New_York`, `Asia/Seoul`, `Europe/London` |

#### Time

| Format | Example |
|---|---|
| 12-hour | `12pm`, `3:30pm`, `9am` |
| 24-hour | `15:00`, `9:30` |
| 4-digit | `1430`, `0900` |

#### Currency

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
│   ├── timezone_action.py      # ct add/remove/format handler
│   ├── currency_dashboard.py   # 'cc' — currency dashboard + conversion
│   ├── currency_action.py      # cc add/remove handler
│   └── converter/
│       ├── data.py             # 60+ locations, country flags, currency data
│       ├── alfred.py           # Alfred JSON output helpers
│       ├── parser.py           # Query parsing & routing
│       ├── timezone.py         # Timezone conversion, timestamp parsing
│       ├── currency.py         # Currency conversion + caching
│       └── favorites.py        # Favorites + format settings
├── build.sh
├── LICENSE
└── README.md
```

## License

MIT
