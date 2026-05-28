#!/usr/bin/env python3
"""
Theme ETF Monitor - data builder.
Pulls daily history from Yahoo Finance (yfinance) and writes data/etf_data.json
consumed by index.html. Run locally or via GitHub Actions.

Output per ETF:
  close          last close
  change_pct     last close vs previous close (%)
  drawdown_pct   last close vs trailing peak close (%), <= 0
  spark          ~40 most recent closes for the sparkline
"""

import json, datetime, sys
import yfinance as yf

# ---- single source of truth: groups, tickers, Korean labels ----
GROUPS = [
    ("섹터", "SECTOR", [
        ("XLK", "정보기술"), ("XLV", "헬스케어"), ("XLF", "금융"),
        ("XLC", "커뮤니케이션"), ("XLY", "소비순환재"), ("XLP", "경기방어주"),
        ("XLI", "산업재"), ("XLU", "유틸리티"), ("XLE", "에너지"),
        ("XLRE", "리츠"), ("XLB", "소재"),
    ]),
    ("가치 / 성장", "STYLE", [
        ("VUG", "대형성장"), ("MGK", "메가캡성장"), ("IWP", "중형성장"),
        ("VBK", "소형성장"), ("VTV", "대형가치"), ("VOE", "중형가치"),
        ("VBR", "소형가치"),
    ]),
    ("성장 테마", "GROWTH THEMES", [
        ("SOXX", "반도체"), ("IGV", "소프트웨어"), ("SKYY", "클라우드"),
        ("AIQ", "인공지능"), ("CIBR", "사이버보안"), ("FINX", "핀테크"),
    ]),
    ("배당", "DIVIDEND", [
        ("VIG", "배당성장"), ("SCHD", "배당퀄리티"), ("NOBL", "배당귀족"),
        ("DVY", "고배당"), ("VNQ", "리츠"), ("JEPQ", "커버드콜"),
    ]),
    ("혁신", "INNOVATION", [
        ("ARKK", "혁신"), ("BOTZ", "로봇"), ("URA", "원전 / 우라늄"),
        ("LIT", "배터리 / 리튬"), ("ICLN", "클린에너지"), ("IBIT", "비트코인"),
    ]),
]

SPARK_LEN = 40


def build_one(ticker: str):
    """Return metrics dict for one ticker, or None on failure."""
    try:
        hist = yf.Ticker(ticker).history(period="2y", interval="1d", auto_adjust=False)
        closes = hist["Close"].dropna()
        if len(closes) < 5:
            print(f"  ! {ticker}: insufficient data", file=sys.stderr)
            return None

        close = float(closes.iloc[-1])
        prev = float(closes.iloc[-2])
        peak = float(closes.max())

        change_pct = (close / prev - 1.0) * 100.0
        drawdown_pct = (close / peak - 1.0) * 100.0  # <= 0

        spark = [round(float(x), 4) for x in closes.iloc[-SPARK_LEN:].tolist()]

        return {
            "close": round(close, 2),
            "change_pct": round(change_pct, 2),
            "drawdown_pct": round(drawdown_pct, 1),
            "spark": spark,
        }
    except Exception as e:  # noqa
        print(f"  ! {ticker}: {e}", file=sys.stderr)
        return None


def main():
    out_groups = []
    as_of = None

    for name, name_en, members in GROUPS:
        etfs = []
        for ticker, label in members:
            print(f"fetching {ticker} ({label}) …")
            m = build_one(ticker)
            if m is None:
                # keep the tile but blank, so layout stays intact
                etfs.append({"ticker": ticker, "label": label,
                             "close": None, "change_pct": None, "drawdown_pct": None})
                continue
            etfs.append({"ticker": ticker, "label": label, **m})
        out_groups.append({"name": name, "name_en": name_en, "etfs": etfs})

    # use today's date in NY; fall back to UTC date
    as_of = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    payload = {
        "as_of": as_of,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "sample": False,
        "groups": out_groups,
    }

    import os
    os.makedirs("data", exist_ok=True)
    with open("data/etf_data.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("\nwrote data/etf_data.json")


if __name__ == "__main__":
    main()
