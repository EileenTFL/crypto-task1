from typing import List, Dict, Any
import pandas as pd

def wei_to_eth(wei: str) -> float:
    try:
        return int(wei) / 10**18
    except Exception:
        return 0.0

def normalize_txlist(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=[
            "hash","time","from","to","value_eth","gas_price_gwei","gas_used","is_error","method_id"
        ])
    df = pd.DataFrame(rows)
    df["time"] = pd.to_datetime(df["timeStamp"].astype(int), unit="s", utc=True)
    df["from"] = df["from"].str.lower()
    df["to"] = df["to"].str.lower()
    df["value_eth"] = df["value"].apply(wei_to_eth)
    df["gas_price_gwei"] = df["gasPrice"].astype(int) / 10**9
    df["gas_used"] = df["gasUsed"].astype(int)
    df["is_error"] = df["isError"].astype(int)
    df["method_id"] = df.get("methodId", None)
    keep = ["hash","time","from","to","value_eth","gas_price_gwei","gas_used","is_error","method_id"]
    return df[keep].sort_values("time", ascending=False).reset_index(drop=True)
