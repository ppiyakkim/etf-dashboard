# Theme ETF Monitor

A terminal-style thematic ETF dashboard. Yahoo Finance data is pulled daily via GitHub Actions, written to a static JSON file, and rendered client-side by GitHub Pages. No server required.

**Live:** [etf.studiochick.net](https://etf.studiochick.net)

---

## What It Shows

| Metric | Description |
|---|---|
| **CLOSE** | Latest closing price |
| **±%** | Daily change vs previous close |
| **FROM PEAK** | Drawdown from 2-year high |
| **Sparkline** | Price history (7D – 1Y, adjustable via slider) |
| **Holdings** | Top 10 holdings treemap (click any tile) |

The summary panel at the top shows up/down count, best/worst daily mover, most resilient ETF, deepest drawdown, and average drawdown by group.

---

## ETF Groups

| Group | Tickers |
|---|---|
| **Sector** | XLK, XLV, XLF, XLC, XLY, XLP, XLI, XLU, XLE, XLRE, XLB |
| **Style** | VUG, MGK, IWP, VBK, VTV, VOE, VBR |
| **Growth Themes** | SOXX, IGV, SKYY, AIQ, CIBR, FINX |
| **Dividend** | VIG, SCHD, NOBL, DVY, VNQ, JEPQ |
| **Innovation** | ARKK, BOTZ, URA, LIT, ICLN, IBIT |
| **Trump Theme** | TSSD, TSNF, TSIC, TSES, TSRS |
| **US ETFs** | VOO, SPY, QQQ, GLD, SCHD, QQQM, BIL, JEPI, TQQQ, SQQQ, IVV |
| **Global ETFs** | VT, VXUS, VEU, VEA, VWO, VGK |
| **Europe** | EZU, EWG, EWU, EWP, EWL, EIS, EWI, EWQ, TUR |
| **APAC** | MCHI, EWJ, EWY, INDA, EWT, EWA, EWS, UAE |

---

## Project Structure

```
etf-dashboard/
├── index.html                    # Single-file dashboard (fetches data/etf_data.json)
├── data/etf_data.json            # Generated data (overwritten by Action daily)
├── scripts/fetch_data.py         # yfinance → JSON builder
└── .github/workflows/update.yml  # Scheduled + manual workflow
```

---

## Setup

1. Push the repo to GitHub.
2. **Settings → Pages → Source: `main` / root** to deploy via GitHub Pages.
3. **Settings → Actions → General → Workflow permissions → Read and write** — required so the bot can commit the updated JSON.
4. **Actions tab → Update ETF data → Run workflow** to generate the first real data. It runs automatically on weekdays thereafter.

The repo ships with sample data so the dashboard renders immediately — the `SAMPLE DATA` badge appears until the first real data commit lands.

---

## Customizing ETFs

Edit the `GROUPS` list at the top of `scripts/fetch_data.py`. The frontend reads only the JSON structure, so adding or removing tickers requires no HTML changes.

```python
GROUPS = [
    ("GROUP NAME", "GROUP NAME", [
        ("TICKER", "Label"),
        ...
    ]),
    ...
]
```

---

## Features

- **Dark / Light mode** toggle, persisted via `localStorage`
- **Chart range slider** — 7D to 1Y, controls all sparklines simultaneously
- **Line / Candlestick toggle** — switch chart type across all tiles
- **Holdings treemap** — click any tile to expand top 10 holdings from Yahoo Finance; hover for company name and weight
- **Responsive grid** — holdings panel inserts directly below the clicked tile's row at any column count
- **Ticker tooltips** — hover the orange ticker label for a brief ETF description

---

## Local Development

```bash
pip install yfinance
python scripts/fetch_data.py    # writes data/etf_data.json
python -m http.server 8000      # open http://localhost:8000
```

---

## Notes

- Yahoo Finance occasionally rate-limits requests. If a single ticker fails, that tile renders empty while all others display normally.
- The drawdown bar is proportional to the absolute drawdown percentage (capped at 100%). It is a visual indicator, not a precise scale.
- OHLC data (open, high, low, close) is stored alongside close prices in the JSON for candlestick rendering — no extra API calls needed.
