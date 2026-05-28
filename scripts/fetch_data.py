#!/usr/bin/env python3
"""Theme ETF Monitor - data builder. Writes data/etf_data.json."""

import json, datetime, sys, os
import yfinance as yf

GROUPS = [
    ("SECTOR", "SECTOR", [
        ("XLK","Info Tech"),("XLV","Healthcare"),("XLF","Financials"),
        ("XLC","Comm Svcs"),("XLY","Cons Disc"),("XLP","Cons Staples"),
        ("XLI","Industrials"),("XLU","Utilities"),("XLE","Energy"),
        ("XLRE","REITs"),("XLB","Materials"),
    ]),
    ("STYLE", "STYLE", [
        ("VUG","Lg Growth"),("MGK","Mega Growth"),("IWP","Mid Growth"),
        ("VBK","Sm Growth"),("VTV","Lg Value"),("VOE","Mid Value"),("VBR","Sm Value"),
    ]),
    ("GROWTH THEMES", "GROWTH THEMES", [
        ("SOXX","Semiconductors"),("IGV","Software"),("SKYY","Cloud"),
        ("AIQ","AI"),("CIBR","Cybersecurity"),("FINX","Fintech"),
    ]),
    ("DIVIDEND", "DIVIDEND", [
        ("VIG","Div Growth"),("SCHD","Div Quality"),("NOBL","Div Aristocrats"),
        ("DVY","High Yield"),("VNQ","REITs"),("JEPQ","Covered Call"),
    ]),
    ("INNOVATION", "INNOVATION", [
        ("ARKK","Innovation"),("BOTZ","Robotics"),("URA","Nuclear/Uranium"),
        ("LIT","Battery/Lithium"),("ICLN","Clean Energy"),("IBIT","Bitcoin"),
    ]),
]

SPARK_LEN = 40

def build_one(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="2y", interval="1d", auto_adjust=False)
        closes = hist["Close"].dropna()
        if len(closes) < 5:
            print(f"  ! {ticker}: insufficient data", file=sys.stderr)
            return None
        close = float(closes.iloc[-1])
        prev  = float(closes.iloc[-2])
        peak  = float(closes.max())
        sl = closes.iloc[-SPARK_LEN:]
        return {
            "close":        round(close, 2),
            "change_pct":   round((close/prev - 1)*100, 2),
            "drawdown_pct": round((close/peak - 1)*100, 1),
            "spark":        [round(float(x),4) for x in sl.tolist()],
            "spark_dates":  [d.strftime("%Y-%m-%d") for d in sl.index],
        }
    except Exception as e:
        print(f"  ! {ticker}: {e}", file=sys.stderr)
        return None

def main():
    out_groups = []
    for name, name_en, members in GROUPS:
        etfs = []
        for ticker, label in members:
            print(f"fetching {ticker} ({label}) …")
            m = build_one(ticker)
            if m is None:
                etfs.append({"ticker":ticker,"label":label,"close":None,"change_pct":None,"drawdown_pct":None})
            else:
                etfs.append({"ticker":ticker,"label":label,**m})
        out_groups.append({"name":name,"name_en":name_en,"etfs":etfs})

    payload = {
        "as_of":        datetime.datetime.utcnow().strftime("%Y-%m-%d"),
        "generated_at": datetime.datetime.utcnow().isoformat()+"Z",
        "sample":       False,
        "groups":       out_groups,
    }
    os.makedirs("data", exist_ok=True)
    with open("data/etf_data.json","w",encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("\nwrote data/etf_data.json")

if __name__ == "__main__":
    main()
