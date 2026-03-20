"""Comprehensive timezone, city, country, and currency data table.

Each location entry maps:
  IANA timezone → city, country, region, tz abbreviations, currency, aliases

Lookup indexes are built at import time for fast searching.
"""

# ─────────────────────────────────────────────────────────────
# Location records
# ─────────────────────────────────────────────────────────────

LOCATIONS = [
    # ── Americas ──────────────────────────────────────────────
    {
        "iana": "America/New_York",
        "city": "New York",
        "country": "United States",
        "region": "Eastern",
        "tz_abbrs": ["EST", "EDT", "ET"],
        "currency": "USD",
        "cc": "US",
        "aliases": ["nyc", "new york", "eastern", "east coast", "manhattan", "boston", "miami", "philadelphia", "atlanta", "washington dc", "dc"],
    },
    {
        "iana": "America/Chicago",
        "city": "Chicago",
        "country": "United States",
        "region": "Central",
        "tz_abbrs": ["CST", "CDT", "CT"],
        "currency": "USD",
        "cc": "US",
        "aliases": ["chicago", "central", "dallas", "houston", "austin", "minneapolis", "nashville", "new orleans"],
    },
    {
        "iana": "America/Denver",
        "city": "Denver",
        "country": "United States",
        "region": "Mountain",
        "tz_abbrs": ["MST", "MDT", "MT"],
        "currency": "USD",
        "cc": "US",
        "aliases": ["denver", "mountain", "salt lake city", "phoenix", "albuquerque", "colorado"],
    },
    {
        "iana": "America/Los_Angeles",
        "city": "Los Angeles",
        "country": "United States",
        "region": "Pacific",
        "tz_abbrs": ["PST", "PDT", "PT"],
        "currency": "USD",
        "cc": "US",
        "aliases": ["la", "los angeles", "pacific", "california", "sf", "san francisco", "seattle", "portland", "vegas", "las vegas", "silicon valley", "west coast"],
    },
    {
        "iana": "America/Anchorage",
        "city": "Anchorage",
        "country": "United States",
        "region": "Alaska",
        "tz_abbrs": ["AKST", "AKDT", "AKT"],
        "currency": "USD",
        "cc": "US",
        "aliases": ["alaska", "anchorage"],
    },
    {
        "iana": "Pacific/Honolulu",
        "city": "Honolulu",
        "country": "United States",
        "region": "Hawaii",
        "tz_abbrs": ["HST", "HAST"],
        "currency": "USD",
        "cc": "US",
        "aliases": ["hawaii", "honolulu", "maui"],
    },
    {
        "iana": "America/Toronto",
        "city": "Toronto",
        "country": "Canada",
        "region": "Eastern",
        "tz_abbrs": ["EST", "EDT"],
        "currency": "CAD",
        "cc": "CA",
        "aliases": ["toronto", "montreal", "ottawa", "quebec"],
    },
    {
        "iana": "America/Vancouver",
        "city": "Vancouver",
        "country": "Canada",
        "region": "Pacific",
        "tz_abbrs": ["PST", "PDT"],
        "currency": "CAD",
        "cc": "CA",
        "aliases": ["vancouver", "bc", "british columbia", "calgary", "edmonton"],
    },
    {
        "iana": "America/Mexico_City",
        "city": "Mexico City",
        "country": "Mexico",
        "region": "Central",
        "tz_abbrs": ["CST", "CDT"],
        "currency": "MXN",
        "cc": "MX",
        "aliases": ["mexico", "mexico city", "cdmx", "guadalajara", "monterrey"],
    },
    {
        "iana": "America/Sao_Paulo",
        "city": "São Paulo",
        "country": "Brazil",
        "region": "Brasilia",
        "tz_abbrs": ["BRT", "BRST"],
        "currency": "BRL",
        "cc": "BR",
        "aliases": ["brazil", "sao paulo", "rio", "rio de janeiro", "brasilia"],
    },
    {
        "iana": "America/Argentina/Buenos_Aires",
        "city": "Buenos Aires",
        "country": "Argentina",
        "region": "Argentina",
        "tz_abbrs": ["ART"],
        "currency": "ARS",
        "cc": "AR",
        "aliases": ["argentina", "buenos aires"],
    },
    {
        "iana": "America/Bogota",
        "city": "Bogotá",
        "country": "Colombia",
        "region": "Colombia",
        "tz_abbrs": ["COT"],
        "currency": "COP",
        "cc": "CO",
        "aliases": ["colombia", "bogota"],
    },
    {
        "iana": "America/Lima",
        "city": "Lima",
        "country": "Peru",
        "region": "Peru",
        "tz_abbrs": ["PET"],
        "currency": "PEN",
        "cc": "PE",
        "aliases": ["peru", "lima"],
    },
    {
        "iana": "America/Santiago",
        "city": "Santiago",
        "country": "Chile",
        "region": "Chile",
        "tz_abbrs": ["CLT", "CLST"],
        "currency": "CLP",
        "cc": "CL",
        "aliases": ["chile", "santiago"],
    },

    # ── Europe ────────────────────────────────────────────────
    {
        "iana": "Europe/London",
        "city": "London",
        "country": "United Kingdom",
        "region": "Greenwich",
        "tz_abbrs": ["GMT", "BST"],
        "currency": "GBP",
        "cc": "GB",
        "aliases": ["uk", "london", "england", "britain", "scotland", "wales", "manchester", "birmingham", "liverpool", "edinburgh"],
    },
    {
        "iana": "Europe/Dublin",
        "city": "Dublin",
        "country": "Ireland",
        "region": "Greenwich",
        "tz_abbrs": ["GMT", "IST"],
        "currency": "EUR",
        "cc": "IE",
        "aliases": ["ireland", "dublin"],
    },
    {
        "iana": "Europe/Lisbon",
        "city": "Lisbon",
        "country": "Portugal",
        "region": "Western Europe",
        "tz_abbrs": ["WET", "WEST"],
        "currency": "EUR",
        "cc": "PT",
        "aliases": ["portugal", "lisbon", "porto"],
    },
    {
        "iana": "Europe/Paris",
        "city": "Paris",
        "country": "France",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "EUR",
        "cc": "FR",
        "aliases": ["france", "paris", "lyon", "marseille"],
    },
    {
        "iana": "Europe/Berlin",
        "city": "Berlin",
        "country": "Germany",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "EUR",
        "cc": "DE",
        "aliases": ["germany", "berlin", "munich", "frankfurt", "hamburg", "munchen", "koln", "cologne"],
    },
    {
        "iana": "Europe/Madrid",
        "city": "Madrid",
        "country": "Spain",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "EUR",
        "cc": "ES",
        "aliases": ["spain", "madrid", "barcelona", "valencia"],
    },
    {
        "iana": "Europe/Rome",
        "city": "Rome",
        "country": "Italy",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "EUR",
        "cc": "IT",
        "aliases": ["italy", "rome", "milan", "roma", "milano", "naples", "florence", "venice"],
    },
    {
        "iana": "Europe/Amsterdam",
        "city": "Amsterdam",
        "country": "Netherlands",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "EUR",
        "cc": "NL",
        "aliases": ["netherlands", "amsterdam", "holland", "rotterdam", "dutch"],
    },
    {
        "iana": "Europe/Brussels",
        "city": "Brussels",
        "country": "Belgium",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "EUR",
        "cc": "BE",
        "aliases": ["belgium", "brussels"],
    },
    {
        "iana": "Europe/Zurich",
        "city": "Zurich",
        "country": "Switzerland",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "CHF",
        "cc": "CH",
        "aliases": ["switzerland", "zurich", "geneva", "bern", "swiss"],
    },
    {
        "iana": "Europe/Stockholm",
        "city": "Stockholm",
        "country": "Sweden",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "SEK",
        "cc": "SE",
        "aliases": ["sweden", "stockholm", "swedish"],
    },
    {
        "iana": "Europe/Oslo",
        "city": "Oslo",
        "country": "Norway",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "NOK",
        "cc": "NO",
        "aliases": ["norway", "oslo", "norwegian"],
    },
    {
        "iana": "Europe/Copenhagen",
        "city": "Copenhagen",
        "country": "Denmark",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "DKK",
        "cc": "DK",
        "aliases": ["denmark", "copenhagen", "danish"],
    },
    {
        "iana": "Europe/Helsinki",
        "city": "Helsinki",
        "country": "Finland",
        "region": "Eastern Europe",
        "tz_abbrs": ["EET", "EEST"],
        "currency": "EUR",
        "cc": "FI",
        "aliases": ["finland", "helsinki", "finnish"],
    },
    {
        "iana": "Europe/Warsaw",
        "city": "Warsaw",
        "country": "Poland",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "PLN",
        "cc": "PL",
        "aliases": ["poland", "warsaw", "krakow", "polish"],
    },
    {
        "iana": "Europe/Prague",
        "city": "Prague",
        "country": "Czech Republic",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "CZK",
        "cc": "CZ",
        "aliases": ["czech", "prague", "czechia"],
    },
    {
        "iana": "Europe/Vienna",
        "city": "Vienna",
        "country": "Austria",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "EUR",
        "cc": "AT",
        "aliases": ["austria", "vienna", "wien"],
    },
    {
        "iana": "Europe/Budapest",
        "city": "Budapest",
        "country": "Hungary",
        "region": "Central Europe",
        "tz_abbrs": ["CET", "CEST"],
        "currency": "HUF",
        "cc": "HU",
        "aliases": ["hungary", "budapest"],
    },
    {
        "iana": "Europe/Athens",
        "city": "Athens",
        "country": "Greece",
        "region": "Eastern Europe",
        "tz_abbrs": ["EET", "EEST"],
        "currency": "EUR",
        "cc": "GR",
        "aliases": ["greece", "athens", "greek"],
    },
    {
        "iana": "Europe/Bucharest",
        "city": "Bucharest",
        "country": "Romania",
        "region": "Eastern Europe",
        "tz_abbrs": ["EET", "EEST"],
        "currency": "RON",
        "cc": "RO",
        "aliases": ["romania", "bucharest"],
    },
    {
        "iana": "Europe/Istanbul",
        "city": "Istanbul",
        "country": "Turkey",
        "region": "Turkey",
        "tz_abbrs": ["TRT"],
        "currency": "TRY",
        "cc": "TR",
        "aliases": ["turkey", "istanbul", "ankara", "turkish"],
    },
    {
        "iana": "Europe/Moscow",
        "city": "Moscow",
        "country": "Russia",
        "region": "Moscow",
        "tz_abbrs": ["MSK"],
        "currency": "RUB",
        "cc": "RU",
        "aliases": ["russia", "moscow", "russian", "st petersburg", "saint petersburg"],
    },
    {
        "iana": "Europe/Kiev",
        "city": "Kyiv",
        "country": "Ukraine",
        "region": "Eastern Europe",
        "tz_abbrs": ["EET", "EEST"],
        "currency": "UAH",
        "cc": "UA",
        "aliases": ["ukraine", "kyiv", "kiev"],
    },

    # ── Asia ──────────────────────────────────────────────────
    {
        "iana": "Asia/Seoul",
        "city": "Seoul",
        "country": "South Korea",
        "region": "Korea",
        "tz_abbrs": ["KST"],
        "currency": "KRW",
        "cc": "KR",
        "aliases": ["korea", "kr", "seoul", "busan", "korean", "south korea", "won"],
    },
    {
        "iana": "Asia/Tokyo",
        "city": "Tokyo",
        "country": "Japan",
        "region": "Japan",
        "tz_abbrs": ["JST"],
        "currency": "JPY",
        "cc": "JP",
        "aliases": ["japan", "jp", "tokyo", "osaka", "japanese", "yen"],
    },
    {
        "iana": "Asia/Shanghai",
        "city": "Shanghai",
        "country": "China",
        "region": "China",
        "tz_abbrs": ["CST"],
        "currency": "CNY",
        "cc": "CN",
        "aliases": ["china", "cn", "shanghai", "beijing", "shenzhen", "guangzhou", "chinese", "yuan", "rmb", "renminbi"],
    },
    {
        "iana": "Asia/Hong_Kong",
        "city": "Hong Kong",
        "country": "Hong Kong",
        "region": "Hong Kong",
        "tz_abbrs": ["HKT"],
        "currency": "HKD",
        "cc": "HK",
        "aliases": ["hong kong", "hk", "hongkong"],
    },
    {
        "iana": "Asia/Taipei",
        "city": "Taipei",
        "country": "Taiwan",
        "region": "Taiwan",
        "tz_abbrs": ["CST", "TWT"],
        "currency": "TWD",
        "cc": "TW",
        "aliases": ["taiwan", "tw", "taipei", "taiwanese"],
    },
    {
        "iana": "Asia/Singapore",
        "city": "Singapore",
        "country": "Singapore",
        "region": "Singapore",
        "tz_abbrs": ["SGT", "SST"],
        "currency": "SGD",
        "cc": "SG",
        "aliases": ["singapore", "sg"],
    },
    {
        "iana": "Asia/Kuala_Lumpur",
        "city": "Kuala Lumpur",
        "country": "Malaysia",
        "region": "Malaysia",
        "tz_abbrs": ["MYT"],
        "currency": "MYR",
        "cc": "MY",
        "aliases": ["malaysia", "kuala lumpur", "kl"],
    },
    {
        "iana": "Asia/Bangkok",
        "city": "Bangkok",
        "country": "Thailand",
        "region": "Indochina",
        "tz_abbrs": ["ICT"],
        "currency": "THB",
        "cc": "TH",
        "aliases": ["thailand", "bangkok", "thai", "baht"],
    },
    {
        "iana": "Asia/Ho_Chi_Minh",
        "city": "Ho Chi Minh City",
        "country": "Vietnam",
        "region": "Indochina",
        "tz_abbrs": ["ICT"],
        "currency": "VND",
        "cc": "VN",
        "aliases": ["vietnam", "ho chi minh", "saigon", "hanoi", "vietnamese", "dong"],
    },
    {
        "iana": "Asia/Jakarta",
        "city": "Jakarta",
        "country": "Indonesia",
        "region": "Western Indonesia",
        "tz_abbrs": ["WIB"],
        "currency": "IDR",
        "cc": "ID",
        "aliases": ["indonesia", "jakarta", "bali", "indonesian", "rupiah"],
    },
    {
        "iana": "Asia/Manila",
        "city": "Manila",
        "country": "Philippines",
        "region": "Philippines",
        "tz_abbrs": ["PHT", "PST"],
        "currency": "PHP",
        "cc": "PH",
        "aliases": ["philippines", "manila", "filipino", "peso"],
    },
    {
        "iana": "Asia/Kolkata",
        "city": "Mumbai",
        "country": "India",
        "region": "India",
        "tz_abbrs": ["IST"],
        "currency": "INR",
        "cc": "IN",
        "aliases": ["india", "mumbai", "delhi", "new delhi", "bangalore", "bengaluru", "indian", "kolkata", "chennai", "hyderabad", "rupee"],
    },
    {
        "iana": "Asia/Karachi",
        "city": "Karachi",
        "country": "Pakistan",
        "region": "Pakistan",
        "tz_abbrs": ["PKT"],
        "currency": "PKR",
        "cc": "PK",
        "aliases": ["pakistan", "karachi", "islamabad", "lahore"],
    },
    {
        "iana": "Asia/Dhaka",
        "city": "Dhaka",
        "country": "Bangladesh",
        "region": "Bangladesh",
        "tz_abbrs": ["BST", "BDT"],
        "currency": "BDT",
        "cc": "BD",
        "aliases": ["bangladesh", "dhaka"],
    },
    {
        "iana": "Asia/Dubai",
        "city": "Dubai",
        "country": "UAE",
        "region": "Gulf",
        "tz_abbrs": ["GST"],
        "currency": "AED",
        "cc": "AE",
        "aliases": ["uae", "dubai", "abu dhabi", "emirates", "gulf"],
    },
    {
        "iana": "Asia/Riyadh",
        "city": "Riyadh",
        "country": "Saudi Arabia",
        "region": "Arabia",
        "tz_abbrs": ["AST"],
        "currency": "SAR",
        "cc": "SA",
        "aliases": ["saudi", "saudi arabia", "riyadh", "jeddah", "mecca"],
    },
    {
        "iana": "Asia/Qatar",
        "city": "Doha",
        "country": "Qatar",
        "region": "Arabia",
        "tz_abbrs": ["AST"],
        "currency": "QAR",
        "cc": "QA",
        "aliases": ["qatar", "doha"],
    },
    {
        "iana": "Asia/Tehran",
        "city": "Tehran",
        "country": "Iran",
        "region": "Iran",
        "tz_abbrs": ["IRST", "IRDT"],
        "currency": "IRR",
        "cc": "IR",
        "aliases": ["iran", "tehran", "persian"],
    },
    {
        "iana": "Asia/Jerusalem",
        "city": "Tel Aviv",
        "country": "Israel",
        "region": "Israel",
        "tz_abbrs": ["IST", "IDT"],
        "currency": "ILS",
        "cc": "IL",
        "aliases": ["israel", "tel aviv", "jerusalem"],
    },

    # ── Oceania ───────────────────────────────────────────────
    {
        "iana": "Australia/Sydney",
        "city": "Sydney",
        "country": "Australia",
        "region": "Eastern Australia",
        "tz_abbrs": ["AEST", "AEDT"],
        "currency": "AUD",
        "cc": "AU",
        "aliases": ["sydney", "australia", "au", "aussie"],
    },
    {
        "iana": "Australia/Melbourne",
        "city": "Melbourne",
        "country": "Australia",
        "region": "Eastern Australia",
        "tz_abbrs": ["AEST", "AEDT"],
        "currency": "AUD",
        "cc": "AU",
        "aliases": ["melbourne"],
    },
    {
        "iana": "Australia/Brisbane",
        "city": "Brisbane",
        "country": "Australia",
        "region": "Eastern Australia",
        "tz_abbrs": ["AEST"],
        "currency": "AUD",
        "cc": "AU",
        "aliases": ["brisbane", "queensland", "gold coast"],
    },
    {
        "iana": "Australia/Perth",
        "city": "Perth",
        "country": "Australia",
        "region": "Western Australia",
        "tz_abbrs": ["AWST"],
        "currency": "AUD",
        "cc": "AU",
        "aliases": ["perth", "western australia"],
    },
    {
        "iana": "Australia/Adelaide",
        "city": "Adelaide",
        "country": "Australia",
        "region": "Central Australia",
        "tz_abbrs": ["ACST", "ACDT"],
        "currency": "AUD",
        "cc": "AU",
        "aliases": ["adelaide", "south australia"],
    },
    {
        "iana": "Pacific/Auckland",
        "city": "Auckland",
        "country": "New Zealand",
        "region": "New Zealand",
        "tz_abbrs": ["NZST", "NZDT"],
        "currency": "NZD",
        "cc": "NZ",
        "aliases": ["new zealand", "nz", "auckland", "wellington", "kiwi"],
    },

    # ── Africa ────────────────────────────────────────────────
    {
        "iana": "Africa/Cairo",
        "city": "Cairo",
        "country": "Egypt",
        "region": "North Africa",
        "tz_abbrs": ["EET"],
        "currency": "EGP",
        "cc": "EG",
        "aliases": ["egypt", "cairo"],
    },
    {
        "iana": "Africa/Lagos",
        "city": "Lagos",
        "country": "Nigeria",
        "region": "West Africa",
        "tz_abbrs": ["WAT"],
        "currency": "NGN",
        "cc": "NG",
        "aliases": ["nigeria", "lagos"],
    },
    {
        "iana": "Africa/Johannesburg",
        "city": "Johannesburg",
        "country": "South Africa",
        "region": "Southern Africa",
        "tz_abbrs": ["SAST"],
        "currency": "ZAR",
        "cc": "ZA",
        "aliases": ["south africa", "johannesburg", "cape town"],
    },
    {
        "iana": "Africa/Nairobi",
        "city": "Nairobi",
        "country": "Kenya",
        "region": "East Africa",
        "tz_abbrs": ["EAT"],
        "currency": "KES",
        "cc": "KE",
        "aliases": ["kenya", "nairobi"],
    },
]

# ─────────────────────────────────────────────────────────────
# Currency records (for currencies not tied to a single location)
# ─────────────────────────────────────────────────────────────

CURRENCIES = [
    {"code": "USD", "name": "US Dollar", "symbol": "$", "aliases": ["dollar", "usd", "buck", "greenback"]},
    {"code": "EUR", "name": "Euro", "symbol": "€", "aliases": ["euro", "eur"]},
    {"code": "GBP", "name": "British Pound", "symbol": "£", "aliases": ["pound", "gbp", "sterling", "quid"]},
    {"code": "JPY", "name": "Japanese Yen", "symbol": "¥", "aliases": ["yen", "jpy"]},
    {"code": "KRW", "name": "Korean Won", "symbol": "₩", "aliases": ["won", "krw"]},
    {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥", "aliases": ["yuan", "cny", "rmb", "renminbi"]},
    {"code": "CAD", "name": "Canadian Dollar", "symbol": "CA$", "aliases": ["cad", "canadian dollar", "loonie"]},
    {"code": "AUD", "name": "Australian Dollar", "symbol": "A$", "aliases": ["aud", "australian dollar", "aussie dollar"]},
    {"code": "NZD", "name": "New Zealand Dollar", "symbol": "NZ$", "aliases": ["nzd", "kiwi dollar"]},
    {"code": "CHF", "name": "Swiss Franc", "symbol": "Fr", "aliases": ["chf", "franc", "swiss franc"]},
    {"code": "HKD", "name": "Hong Kong Dollar", "symbol": "HK$", "aliases": ["hkd"]},
    {"code": "SGD", "name": "Singapore Dollar", "symbol": "S$", "aliases": ["sgd"]},
    {"code": "SEK", "name": "Swedish Krona", "symbol": "kr", "aliases": ["sek", "krona"]},
    {"code": "NOK", "name": "Norwegian Krone", "symbol": "kr", "aliases": ["nok", "krone"]},
    {"code": "DKK", "name": "Danish Krone", "symbol": "kr", "aliases": ["dkk"]},
    {"code": "PLN", "name": "Polish Złoty", "symbol": "zł", "aliases": ["pln", "zloty"]},
    {"code": "CZK", "name": "Czech Koruna", "symbol": "Kč", "aliases": ["czk", "koruna"]},
    {"code": "HUF", "name": "Hungarian Forint", "symbol": "Ft", "aliases": ["huf", "forint"]},
    {"code": "TRY", "name": "Turkish Lira", "symbol": "₺", "aliases": ["try", "lira", "turkish lira"]},
    {"code": "RUB", "name": "Russian Ruble", "symbol": "₽", "aliases": ["rub", "ruble", "rouble"]},
    {"code": "INR", "name": "Indian Rupee", "symbol": "₹", "aliases": ["inr", "rupee"]},
    {"code": "IDR", "name": "Indonesian Rupiah", "symbol": "Rp", "aliases": ["idr", "rupiah"]},
    {"code": "MYR", "name": "Malaysian Ringgit", "symbol": "RM", "aliases": ["myr", "ringgit"]},
    {"code": "THB", "name": "Thai Baht", "symbol": "฿", "aliases": ["thb", "baht"]},
    {"code": "PHP", "name": "Philippine Peso", "symbol": "₱", "aliases": ["php", "peso"]},
    {"code": "VND", "name": "Vietnamese Dong", "symbol": "₫", "aliases": ["vnd", "dong"]},
    {"code": "TWD", "name": "Taiwan Dollar", "symbol": "NT$", "aliases": ["twd", "nt"]},
    {"code": "BRL", "name": "Brazilian Real", "symbol": "R$", "aliases": ["brl", "real"]},
    {"code": "MXN", "name": "Mexican Peso", "symbol": "MX$", "aliases": ["mxn"]},
    {"code": "ARS", "name": "Argentine Peso", "symbol": "AR$", "aliases": ["ars"]},
    {"code": "CLP", "name": "Chilean Peso", "symbol": "CL$", "aliases": ["clp"]},
    {"code": "COP", "name": "Colombian Peso", "symbol": "CO$", "aliases": ["cop"]},
    {"code": "PEN", "name": "Peruvian Sol", "symbol": "S/", "aliases": ["pen", "sol"]},
    {"code": "ZAR", "name": "South African Rand", "symbol": "R", "aliases": ["zar", "rand"]},
    {"code": "AED", "name": "UAE Dirham", "symbol": "د.إ", "aliases": ["aed", "dirham"]},
    {"code": "SAR", "name": "Saudi Riyal", "symbol": "﷼", "aliases": ["sar", "riyal"]},
    {"code": "ILS", "name": "Israeli Shekel", "symbol": "₪", "aliases": ["ils", "shekel"]},
    {"code": "EGP", "name": "Egyptian Pound", "symbol": "E£", "aliases": ["egp"]},
    {"code": "NGN", "name": "Nigerian Naira", "symbol": "₦", "aliases": ["ngn", "naira"]},
    {"code": "KES", "name": "Kenyan Shilling", "symbol": "KSh", "aliases": ["kes", "shilling"]},
    {"code": "UAH", "name": "Ukrainian Hryvnia", "symbol": "₴", "aliases": ["uah", "hryvnia"]},
    {"code": "RON", "name": "Romanian Leu", "symbol": "lei", "aliases": ["ron", "leu"]},
    {"code": "PKR", "name": "Pakistani Rupee", "symbol": "Rs", "aliases": ["pkr"]},
    {"code": "BDT", "name": "Bangladeshi Taka", "symbol": "৳", "aliases": ["bdt", "taka"]},
    {"code": "QAR", "name": "Qatari Riyal", "symbol": "QR", "aliases": ["qar"]},
    {"code": "IRR", "name": "Iranian Rial", "symbol": "﷼", "aliases": ["irr", "rial"]},
]

# Currencies with 0 decimal places
ZERO_DECIMAL_CURRENCIES = {"JPY", "KRW", "VND", "IDR", "CLP", "ISK", "HUF", "COP"}


# ─────────────────────────────────────────────────────────────
# Lookup indexes (built once at import time)
# ─────────────────────────────────────────────────────────────

def _build_indexes():
    """Build fast lookup dictionaries from LOCATIONS and CURRENCIES."""

    # tz_abbr (upper) → first matching location
    tz_to_location = {}
    # alias (lower) → location
    alias_to_location = {}
    # city (lower) → location
    city_to_location = {}
    # country code (upper) → location
    cc_to_location = {}
    # currency code (upper) → location (first match)
    curr_to_location = {}
    # iana → location
    iana_to_location = {}
    # all searchable terms → location (for ct add search)
    search_index = {}  # term (lower) → list of locations

    def _add_search(term, loc):
        term = term.lower().strip()
        if term:
            search_index.setdefault(term, [])
            if loc not in search_index[term]:
                search_index[term].append(loc)

    for loc in LOCATIONS:
        iana_to_location[loc["iana"]] = loc

        for abbr in loc["tz_abbrs"]:
            upper = abbr.upper()
            if upper not in tz_to_location:
                tz_to_location[upper] = loc
            _add_search(abbr, loc)

        city_lower = loc["city"].lower()
        city_to_location[city_lower] = loc
        _add_search(loc["city"], loc)

        _add_search(loc["country"], loc)

        cc_upper = loc["cc"].upper()
        if cc_upper not in cc_to_location:
            cc_to_location[cc_upper] = loc

        curr_upper = loc["currency"].upper()
        if curr_upper not in curr_to_location:
            curr_to_location[curr_upper] = loc
        _add_search(loc["currency"], loc)

        _add_search(loc["cc"], loc)

        for alias in loc.get("aliases", []):
            alias_lower = alias.lower()
            alias_to_location[alias_lower] = loc
            _add_search(alias, loc)

    # Currency aliases → location
    for curr in CURRENCIES:
        code = curr["code"].upper()
        for alias in curr.get("aliases", []):
            _add_search(alias, curr_to_location.get(code))

    return {
        "tz": tz_to_location,
        "alias": alias_to_location,
        "city": city_to_location,
        "cc": cc_to_location,
        "currency": curr_to_location,
        "iana": iana_to_location,
        "search": search_index,
    }


_IDX = _build_indexes()


def resolve_location(name):
    """Resolve a name/abbreviation/alias to a location record.
    Returns the location dict or None.
    """
    if not name:
        return None
    s = name.strip()
    lower = s.lower()
    upper = s.upper()

    # Direct IANA
    if s in _IDX["iana"]:
        return _IDX["iana"][s]

    # Timezone abbreviation
    if upper in _IDX["tz"]:
        return _IDX["tz"][upper]

    # City name
    if lower in _IDX["city"]:
        return _IDX["city"][lower]

    # Alias
    if lower in _IDX["alias"]:
        return _IDX["alias"][lower]

    # Country code
    if upper in _IDX["cc"]:
        return _IDX["cc"][upper]

    # Currency code
    if upper in _IDX["currency"]:
        return _IDX["currency"][upper]

    return None


def search_locations(query):
    """Search locations by any term. Returns list of unique location dicts."""
    if not query:
        return []
    lower = query.strip().lower()

    # Exact match first
    results = []
    seen_iana = set()

    def _add(loc):
        if loc and loc["iana"] not in seen_iana:
            results.append(loc)
            seen_iana.add(loc["iana"])

    # Exact matches
    for loc in _IDX["search"].get(lower, []):
        if loc:
            _add(loc)

    # Prefix/substring matches
    for term, locs in _IDX["search"].items():
        if lower in term or term.startswith(lower):
            for loc in locs:
                if loc:
                    _add(loc)

    return results[:20]  # Limit results


def get_iana(name):
    """Resolve name to IANA timezone string."""
    loc = resolve_location(name)
    if loc:
        return loc["iana"]

    # Try direct IANA
    if "/" in name:
        return name

    # UTC special case
    if name.upper() == "UTC":
        return "UTC"

    return None


def get_currency_for_location(name):
    """Get the currency code for a location/country/alias."""
    loc = resolve_location(name)
    if loc:
        return loc.get("currency")
    return None


def format_location(loc, tz_abbr=None):
    """Format a location for display: 'City, Country (TZ_ABBR)'."""
    if not tz_abbr:
        tz_abbr = loc["tz_abbrs"][0] if loc.get("tz_abbrs") else ""
    return f"{loc['city']}, {loc['country']} ({tz_abbr})"
