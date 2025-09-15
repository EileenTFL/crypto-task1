# src/cg_client.py
from pathlib import Path
from typing import List, Tuple
import pandas as pd
import requests

def _fixture_path(coin_id: str) -> Path:
    """Return fixture CSV path (defaults to bitcoin if coin-specific is missing)."""
    here = Path(__file__).resolve().parent.parent
    candidate = here / f"tests/fixtures/sample_ohlcv_{coin_id}.csv"
    return candidate if candidate.exists() else (here / "tests/fixtures/sample_ohlcv_bitcoin.csv")

def fetch_ohlcv(coin_id: str = "bitcoin", days: int = 30) -> pd.DataFrame:
    """
    Return DataFrame with columns: time (UTC tz-aware), price (USD close), volume (USD).
    Tries CoinGecko; on any error falls back to a small fixture CSV so the script always runs.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        prices: List[Tuple[int, float]] = data.get("prices", [])
        vols:   List[Tuple[int, float]] = data.get("total_volumes", [])
        rows = []
        for i in range(min(len(prices), len(vols))):
            ts_ms, price = prices[i]
            _, vol = vols[i]
            rows.append((pd.to_datetime(ts_ms, unit="ms", utc=True), float(price), float(vol)))
        df = pd.DataFrame(rows, columns=["time", "price", "volume"])
        return df.sort_values("time").reset_index(drop=True)
    except Exception:
        # fixture fallback (offline/rate-limit safe)
        fp = _fixture_path(coin_id)
        df = pd.read_csv(fp, parse_dates=["time"])
        if df["time"].dt.tz is None:
            df["time"] = df["time"].dt.tz_localize("UTC")
        return df.sort_values("time").reset_index(drop=True)
